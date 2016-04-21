#!/usr/bin/env python
from pyasp.asp import *
from io import StringIO
import csv

# TODO ya des numeros Gi qui se balladent en tant que uniprot..=> voir le todo pr abruti ds recup ec..

# TODO on peut envoyer les trucs asp en strings, regarder le tuto
# TODO matter si ya bien autant de ref que d'ec..

"""
#Memmo base#
common_name(reaction_id or enzyme_id or pathway_id or compound_id , common_name).
direction(reaction_id, reaction_direction).
ec_number(reaction_id, ec(x,x,x,x) ou ec(x,x,x)).
reactant(reaction_id, reactant_id, stochio)
product(reaction_id, product_id, stochio).
in_pathway(reaction_id, pathway_id).
catalysed_by(reaction_id, enzyme_id).
uniprotID(enzyme_id, uniprot_id).
is_a(class or compound, class_id).
is_a(pathway_id, pathway_id).

#Memmo ma base#
uniprot( ec(2,1,1,72),"A0A0L7Y7H5").
num_access("NC_020229.1","A0A0L7Y7H5").
"""
###########
# memmo ASP
###########
"""
Mettre des Maj aux noms de variables..
"""

goptions = ''  # soluce max gringo
soptions = ''  # solutions max solveur
solver = Gringo4Clasp(gringo_options=goptions, clasp_options=soptions)

#le test ASP en fichier virtuel..
testo = """
"""
test_io = StringIO(testo)

# Liste des fichiers asp
hidden = 'ASP/hidden.lp'
base = 'ASP/metacyc_18.5.lp'
query = 'ASP/explore.lp'
test = 'ASP/test.lp'
metagdb = 'ASP/ec_uni.lp'


# Solver
result = solver.run([hidden, base, test, metagdb], collapseTerms=True, collapseAtoms=False)

# impression de sortie ASP
# for termm in result[0]:
#     print(termm)
#     print(termm.arguments)
#     print(termm.predicate)

# Impression du nombre d'élément en sortie
print("Nombre: ", len(result[0]))

from matplotlib import pyplot as plt
import numpy as np

class Resultats:

    def __init__(self, m_result, m_list_acc):
        self.result = m_result[0]
        self.list_access = m_list_acc  # osef au final
        self.dico_vit = {}
        self.list_ec_vit()
        self.dico_souche = {}
        self.bdd_temp()

    def list_ec_vit(self):
        """
        Associe une clef(la vitamine) à une valeur, les num ec qui sont contenus dans cette vitamines
        Pour les ec des pathway de vitamine ( enzymeV(V,Ec) )
        :return:
        """
        for term in self.result:  # itère les termes
            if term.predicate == "enzymeV":  # ne retient que les terms enzymeV
                self.dico_vit[term.arguments[0]] = self.dico_vit.get(term.arguments[0], []) + [term.arguments[1]]
                # si la cle n'existe pas, le get initialise une liste vide
        print(self.dico_vit)

    def bdd_temp(self):
        """
        full_match(V,S,T,Ec)
        Fait en gros une petite bdd temporaire
        dico_souche: {'b9':{LEKW00000000.1: [[list_ec_full], [list_ec_part]] ,... }, ...}
        """
        for term in self.result:  # itère les termes
            if term.predicate == "full_match":  # ne retient que les terms full_match !!
                self.dico_souche[term.arguments[0]] = self.dico_souche.get(term.arguments[0], {})

                self.dico_souche[term.arguments[0]][term.arguments[1]] = \
                    l = self.dico_souche[term.arguments[0]].get(term.arguments[1], [[], []])
                l[0] += [term.arguments[3]]

            if term.predicate == "rest_match":
                self.dico_souche[term.arguments[0]] = self.dico_souche.get(term.arguments[0], {})
                # initialisation de la clef vit
                self.dico_souche[term.arguments[0]][term.arguments[1]] = \
                    l = self.dico_souche[term.arguments[0]].get(term.arguments[1], [[], []])
                l[1] += [term.arguments[3]]
        print(self.dico_souche)

    def tab_comptage(self, vitamin=None):
        """
        Faut le sortir en csv maintenant...
        :param vitamin:
        :return:
        """
        if vitamin is None:
            for key_vit in sorted(self.dico_souche.keys()):  # itère les vitamines, sorted pr eviter l'aleatoire
                for key_souche in sorted(self.dico_souche[key_vit].keys()):
                    print(key_vit, key_souche)
                    print("Nb_full", len(self.dico_souche[key_vit][key_souche][0]))
                    print("Nb_rest", len(self.dico_souche[key_vit][key_souche][1]))
        else:
            for key_souche in sorted(self.dico_souche[vitamin].keys()):
                    print(vitamin, key_souche)
                    print("Nb_full", len(self.dico_souche[vitamin][key_souche][0]))
                    print("Nb_rest", len(self.dico_souche[vitamin][key_souche][1]))

    def tab_qualit(self):

        for vit in sorted(self.dico_souche.keys()):
            list_souches = []
            for souche in sorted(self.dico_souche[vit].keys()):
                list_ec = []
                for ec_vit in self.dico_vit[vit]:
                    if ec_vit in self.dico_souche[vit][souche][0]:
                        # print("full")
                        list_ec.append(100)
                    elif ec_vit in self.dico_souche[vit][souche][1]:
                        # print("part")
                        list_ec.append(50)
                    else:
                        # print("non")
                        list_ec.append(0)
                list_souches.append(list_ec)
            print(list_souches)
            self.out_csv(vit, list_souches, self.dico_vit[vit], sorted(self.dico_souche[vit].keys()))
            self.heatmap(list_souches, self.dico_vit[vit], sorted(self.dico_souche[vit].keys()))
            # yield list_souches

    def correspondance_souche(self):
        pass

    def out_csv(self, vit, p_listsouche, p_headcol, p_headligne):
        """
        bon au final passer par numpy emmerde plus qu'autre chose..mais ca marche
        :param vit:
        :param p_listsouche:
        :param p_headcol:
        :param p_headligne:
        :return:
        """
        matrice = np.array(p_listsouche, dtype='U24')  # passe en unicode
        headcol = ';'.join(p_headcol)  # header de num ec en string
        rows = np.array(p_headligne, dtype='U24')[:, np.newaxis]  # les coms de souche en array s20

        np.savetxt(
            'ASP/tab_csv_'+vit+'.csv',           # file name, ac nom vit
            np.hstack((rows, matrice)),           # ajoute les row tiles
            fmt='%s',             # formatattage  %.2f
            header=headcol,         # le header
            delimiter=';',          # column delimiter
            newline='\n',           # new line character
            footer='',   # fin fichier
            comments='#; ',          # le ; permet de décaller le header
            )

    def heatmap(self, p_list_souches, p_head_col, p_head_ligne):
        """
        A améliorer, sauvegarder les images, mettre plusieurs map sur une seule fenetre, ajouter un titre,
        mettre de meilleures couleurs et un quadrillage
        :param p_list_souches:
        :param p_head_col:
        :param p_head_ligne:
        :return:
        """
        # tester add subplot pour avoir les trois plots en mm temps

        matrice = np.array(p_list_souches)  # transforme une liste de liste en matrice
        # plt.figure(figsize=(5, 5))
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(matrice, vmin=0, vmax=200)  # intialisation + echelle de couleur

        # cax = plt.axes([0.9, 0.13, 0.04, 0.7]) #position colormap
        # plt.colorbar(cax=cax)

        # on met les petits traits des légendes
        ax.set_xticks(np.arange(matrice.shape[1])+0.5, minor=False)
        ax.set_yticks(np.arange(matrice.shape[0])+0.5, minor=False)
        # on ajoute les labels
        ax.set_xticklabels(p_head_col, minor=False)
        ax.set_yticklabels(p_head_ligne, minor=False)

        # on met les axes en mode tableau
        # les ec de la colone ne sont pas triés=> ils sont pas tjr dans le mm ordre mais pas d'incohérence
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        # (print(dir(plt.figure())))
        plt.show()




with open('exemple/ListeAccess', mode='r') as fichaccess:  # ca aussi on sen fout
    listacc = [i.strip() for i in fichaccess]
    inst_resul = Resultats(result, listacc)
    # inst_resul.tab_comptage()
    inst_resul.tab_qualit()



"""
en gros, ce qu'il faut:

{'b9':{LEKW00000000.1: [[list_ec_full], [list_ec_part]] ,... } }

ou

{'b9':[ [LEKW00000000.1 , [list_ec_full], [list_ec_part]] ,...] }
"""


"""
LEKW00000000.1
NZ_CM003439.1
NZ_CP010528.1
NZ_CP009236.1
NC_021514.1
NC_020229.1
NC_014554.1
NC_021224.2
NC_012984.1
AL935263.2
FN806773
"""