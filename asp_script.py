#!/usr/bin/env python
from pyasp.asp import *
from matplotlib import pyplot as plt
import numpy as np
import csv
import itertools

# TODO ya des numeros Gi qui se balladent en tant que uniprot..=> voir le todo pr abruti ds recup ec..

# TODO on peut envoyer les trucs asp en strings, regarder le tuto
# TODO matter si ya bien autant de ref que d'ec..

# TODO networkx pour le graph

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
# Les tod-o
# - Convertir les sbml en ASP
# integrer le noms des souches dans la bdd => OK
# remonter les voies metabo via asp, trouver des voies alternatives
# preparer les fichiers fasta ac proteines

# regarder l'ordre de croissance des bactéries ?
# regarder les positions sur le génome des enzymes?
# chopper des publis sur les tas de lards
# affichache des voies metabo avec cytoscape (regarder le mail et la publi)
# Et si au lieu de prendre des numéros ec séparément, on changeait d'échelle pour faire le calcul sur des petites
# portions de pathways? et que pour chaque bacteries, on représente sur différentes lignes ces bouts de patways,
# comme pr les coop de bactéries des coop de pathways?
# pouvoir inserer des limites de diffusion
# faire l'affichage des résultats de la question 2
# HMM des enzymes de metacyc (jeane got) OK, pas vraiment de résultats todo qd mm regarder si ya des infos en plus..
# reunion 7 ou 8 juin

goptions = ''  # soluce max gringo
soptions = '--opt-mode=optN'  # solutions max solveur todo -cc vitamin=b12 pour ecraser la constante
solver = Gringo4Clasp(gringo_options=goptions, clasp_options=soptions)

# Liste des fichiers asp
hidden = 'ASP/hidden.lp'
base = 'ASP/metacyc_18.5.lp'
query = 'ASP/explore.lp'
test = 'ASP/test_data.lp'
metagdb = 'ASP/ec_uni.lp'
prog = 'ASP/programmeASP.lp'
questions = 'ASP/questions.lp'
question3 = 'ASP/question3.lp'
hmm = 'ASP/hmm.lp'

# itertools product, pour les listes intent imbriquées
# todo ya des '"' autour des num_acc..
# todo faire les initia des dico avec des = et des methodes statiques

# Solver
result = solver.run([hidden, base, prog, metagdb, questions], collapseTerms=True, collapseAtoms=False)
# result = solver.run([hidden, base, prog, metagdb], collapseTerms=True, collapseAtoms=False)

# Solver de test:
# result = solver.run([test, prog, questions], collapseTerms=True, collapseAtoms=False)
# result = solver.run([hidden, base, prog, hmm, questions], collapseTerms=True, collapseAtoms=False)
# result = solver.run([hidden, base, prog, hmm], collapseTerms=True, collapseAtoms=False)

#  pourquoi dans certains cas result 0 n'existe pas?? pour les cas ou pas de modèle
# impression de sortie ASP
for termm in result[0]:
    print(termm)
#     print(termm.arguments)
#     print(termm.predicate)

# Impression du nombre d'élément en sortie
print("Nombre: ", len(result[0]))


class Resultats:

    def __init__(self, m_result):
        self.result = m_result[0]  # la sortie ASP (seulement 1 modèle)
        self.models = m_result  # les différents modèles
        self.dico_vit = {}  # init dico_vit
        self.list_ec_vit()  # remplissage dico_vit(clé:vit ; val: num_ec de la vit)
        self.dico_souche = {}  # init dico_souche
        self.bdd_temp()  # remplissage dico_souche
        self.dico_trad = {}  # init dico de corespondance de souches
        self.correspondance_souche()  # pas oublier le remplissage


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

        faut mieux commenter le code car j'y comprend plus rien là
        defaultdict a regarder
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
        Sort une table avec les vitamines, et pr chaque vit les souches ac le nb de full et de rest match.
        On peut sortir le tableau avec une vitamine spécifique


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
        """
        Permet de mettre en forme les données pour faire un tableau de présence/abs d'enzymes
        dico_souche: {'b9':{LEKW00000000.1: [[list_ec_full], [list_ec_part]] ,... }, ...}
        UTILISE:
        - out_csv()
        - heatmap()
        :return:
        """
        for vit in sorted(self.dico_souche.keys()):  # itère dans l'ordre les vitamines
            list_souches = []
            # print(len(self.dico_souche[vit].keys()))  # il manque une souche pour la b9..
            for souche in sorted(self.dico_souche[vit].keys()):  # itère dans l'ordre les souches
                list_ec = []
                for ec_vit in sorted(self.dico_vit[vit]):  # dico_vit ici, liste des nums ec de la vit
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
            # try:
            #     headcol = [';'.join(self.dico_trad[sch.replace('"', '')]) for sch in sorted(self.dico_souche[vit].keys())]
            #     # je met le sorted car c aussi sorted dans "list_souches"
            #     # ; "matrice" ; header colones ; header lignes
            #     self.out_csv(vit, list_souches, self.dico_vit[vit], headcol)
            #     self.heatmap(list_souches, self.dico_vit[vit], headcol)
            # except:
            #     self.out_csv(vit, list_souches, self.dico_vit[vit], sorted(self.dico_souche[vit].keys()))
            #     self.heatmap(list_souches, self.dico_vit[vit], sorted(self.dico_souche[vit].keys()))
            #     print("\033[95m Problem dico trad! \033[0m")  # petite coloration..

            # pour l'instant c plus pratique.
            # faudra faire gaffe avec tous ces sorted..
            self.out_csv(vit, list_souches, sorted(self.dico_vit[vit]), sorted(self.dico_souche[vit].keys()))
            self.heatmap(list_souches, sorted(self.dico_vit[vit]), sorted(self.dico_souche[vit].keys()))

    def correspondance_souche(self):
        """
        Remplit dico trad (clé: num_acc ; valeur: [espèce,souche] )
        Utilise un fichier csv pour se charger
        :return:
        """
        # todo elle veut plus de colones
        with open("ASP/trad_souches/correspondance_souches.csv", 'r') as fich_dico:
            reader = csv.reader(fich_dico, delimiter=';')
            for i in reader:
                self.dico_trad[i[2]] = [i[0], i[1]]


    def out_csv(self, vit, p_listsouche, p_headcol, p_headligne):
        """
        Enregistre via numpy les data de tab_qualit en csv, et l'enregistre dans un fichier ac le nom de la bact
        bon au final passer par numpy emmerde plus qu'autre chose..mais ca marche
        :param vit:
        :param p_listsouche:
        :param p_headcol:
        :param p_headligne:
        :return:
        """

        matrice = np.array(p_listsouche, dtype='U128')  # passe en unicode (att, limite 128 carac...)
        headcol = ';'.join(p_headcol)  # header de num ec en string
        rows = np.array(p_headligne, dtype='U128')[:, np.newaxis]  # les coms de souche en array s20

        np.savetxt(
            'ASP/Output/tab_csv_'+vit.replace('"', '')+'.csv',           # file name, ac nom vit, et sans ""
            np.hstack((rows, matrice)),           # ajoute les row tiles
            fmt='%s',             # formatattage  %.2f
            header=headcol,         # le header
            delimiter=';',          # column delimiter
            newline='\n',           # new line character
            footer='',   # fin fichier
            comments='Genre/especes; Souche ; ',          # le ; permet de décaller le header
            )

    def heatmap(self, p_list_souches, p_head_col, p_head_ligne):
        """
        A améliorer, sauvegarder les images, mettre plusieurs map sur une seule fenetre, ajouter un titre,
        mettre de meilleures couleurs et un quadrillage
        :param p_list_souches:  # valeur de couleur de la heatmap
        :param p_head_col:  # les noms des ec
        :param p_head_ligne:  # les noms des souches
        :return:
        """
        # tester add subplot pour avoir les trois plots en mm temps
        print("nb_souches: ", len(p_list_souches))

        p_head_ligne = [self.dico_trad.get(souche.strip('"')) for souche in p_head_ligne]  # traduction nom souches

        # non ya pas le mm nombre de souches.. 64 pour b9, NZ_LKLZ01000013.1 manque
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


    def tableau_q1(self):
        """
        Faut évidement activer le show "completeStrainV"
        """
        dico_q1 = {}  # cle: vit ; valeurs: souches
        for term in self.result:  # itère les termes du modèle
            if term.predicate == "completeStrainV":
                # dico_q1[term.arguments[1]] = dico_q1.get(term.arguments[1], []) + [term.arguments[0]]
                # avec traduction des souches
                dico_q1[term.arguments[1]] = dico_q1.get(term.arguments[1], []) + [self.dico_trad[term.arguments[0].strip('"')]]
        print(dico_q1)
        with open('ASP/Output/tab_q1.csv', 'w', newline='') as sortie_q1:  # éviter les lignes blanches
            writter = csv.writer(sortie_q1)
            for vit in dico_q1.keys():
                writter.writerow(vit)
                for souche in sorted(dico_q1[vit]):
                    writter.writerow(souche)


    """
    faut que je trouve le minimum, puis que je filtre selon ce minimum=> pas besoin au final ya que des minis..
    par contre faut imprimer enzymV, pour avoir self.dico_vit
    """
    # todo traduire le nom des souches..
    def tableau_q2(self):
        list_vit = ['b9', 'b12', 'k2_7']

        for vit in list_vit:  # on itère les vitamines
            print('#########################'+vit+'##################################################')
            yield vit
            for model in self.models:  # on itère les modèles
                # print(dir(model))
                # print(model.score)  # bizare, j'ai dit bizare ils ont tous le mm score.. tant mieux du coup
                list_ec_model = []
                for ec in sorted(self.dico_vit[vit]):  # itère ecV
                    list_souche_ec = []

                    for atom in model:  # défile les prédicats du modèle

                        if atom.predicate == 'minStrainVitamin' and atom.arguments[1] == vit:  # si bon predicat et bne vit

                            if ec == atom.arguments[2]:  # si ecV == ecS
                                print(atom)
                                list_souche_ec.append(atom.arguments[0])  # on ajoute le nom de la souche
                    list_ec_model.append(list_souche_ec)
                print('\n Fin modèle')
                # print(list_ec_model)
                yield list_ec_model



    # todo faudra faire un set pour éliminer les doublons.. pk yen a d'ailleurs? ya plus de doublons, tt a refaire
    """
    necessite  total match etc (j'ai désactivé les heatmaps)
    minstrainvit/2.
    """
    def tableau_q2_bis(self):
        print("################Tableau Vitamin #################")
        list_vit = ['b9', 'b12', 'k2_7']
        # todo trouver la variable (vitamine)
        for vit in list_vit:
            print('#########################'+vit+'##################################################')
            yield vit
            yield list(sorted(self.dico_vit[vit]))
            list_model = []
            for model in self.models:
                # print('##########Modèle')
                list_ec_model = []
                for ecc in sorted(self.dico_vit[vit]):
                    list_souche_ec = []
                    for atom in model:
                        if atom.predicate == 'minStrainVitamin' and atom.arguments[1] == vit:  # si bon predicat et bne vit
                            # print(atom)
                            list_ec_souche = list(itertools.chain.from_iterable([ec for ec in self.dico_souche[vit][atom.arguments[0]]]))
                            # et encore du bourrin..
                            # print(list_ec_souche)
                            if ecc in list_ec_souche:
                                # print(atom, ecc)
                                list_souche_ec.append(atom.arguments[0])
                    list_ec_model.append(list_souche_ec)
                # print(list_ec_model)
                # yield [''.join(str([self.dico_trad[souche.replace('"', '')] for souche in listsouche])) for listsouche in list_ec_model]

                # list_model.append(tuple([''.join(str([self.dico_trad[souche.replace('"', '')] for souche in listsouche])) for listsouche in list_ec_model]))

                list_model.append([''.join([self.dico_trad[souche.replace('"', '')] for souche in listsouche]) for listsouche in list_ec_model])

                # jamais rien vu de plus beau..
            yield from (mod for mod in list_model)
            # for mod in list_model:
            #     yield self.affichage_legende(mod)

    def tableau_q2_final(self, question):
        """
        fait aussi la question 3..
        faudra dire à clingo d'iérer les vitamines
        """
        print("#########Q2final")
        list_ec = []
        for atom in self.models[1]:  # remplit la liste d'ec de la vit
                if atom.predicate == question:
                    list_ec.append(atom.arguments[2])  # ajout l'ec
        list_ec = sorted(set(list_ec))  # tri des ec, uniques

        list_model = []

        for model in self.models:  # itère les diff solutions
            list_souches = {}
            for ec in list_ec:
                for atom in model:
                    if atom.predicate == question and atom.arguments[2] == ec:
                        list_souches[ec] = list_souches.get(ec, []) + [atom.arguments[0]]
            # print(list_souches)
            list_model.append(list_souches)
        # print(list_model)

        # la sortie:
        yield list_ec  # le header
        for model in list_model:
            sortie_model = []
            for ec in list_ec:
                trad = [self.dico_trad[sou.strip('"')] for sou in model[ec]]
                sortie_model.append(trad)
            yield sortie_model
        # todo faire une sortie plus classe avec légende,






    def affichage_legende(self, mod):
        list_union_souche = {}
        for ec in mod:
            for souche, idd in enumerate(ec):
                if souche not in list_union_souche:
                    list_union_souche[souche] = idd
        print(list_union_souche)
        list_return = []
        list_return.append(list_union_souche)
        for ec in mod:
            ls_numsouche = []

            if list_union_souche.get(i, 'biz') in ec:
                ls_numsouche.append(i)
            list_return.append(ls_numsouche)

        return list_return


####################################
# MAIN
####################################

# instanciation
inst_resul = Resultats(result)

# inst_resul.tab_comptage()
inst_resul.tab_qualit()
inst_resul.tableau_q1()

# inst_resul.tableau_q2_bis()
q2 = inst_resul.tableau_q2_final('minStrainVitamin')  # 'minStrainVitamin' ou minStrain pr q3..
# [print(ligne) for ligne in q2]

# faudra le mettre dans la fonction
with open('ASP/Output/tab_Q2.csv', 'w', newline='') as sortie_q2:
    writter = csv.writer(sortie_q2, delimiter=';')
    for ligne in q2:
        # print(ligne)
        writter.writerow(ligne)


# todo surveille au niveau de la k2 1ere vit on dirait que yavait de l'aléatoire.(en fait non)
# todo au niveau des souches de la heatmap, elle n'affiche pas les souches vides

"""
en gros, ce qu'il faut:

{'b9':{LEKW00000000.1: [[list_ec_full], [list_ec_part]] ,... } }

ou

{'b9':[ [LEKW00000000.1 , [list_ec_full], [list_ec_part]] ,...] }
"""
