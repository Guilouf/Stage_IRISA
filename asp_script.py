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
                if term.arguments[0] not in self.dico_vit:  # on ajoute les numéros ec associés à une clé de dico par vit
                    # on est au niveau de la valeur de la clé vit
                    self.dico_vit[term.arguments[0]] = [term.arguments[1]]
                else:
                    self.dico_vit[term.arguments[0]] += [term.arguments[1]]
        print(self.dico_vit)

    def bdd_temp(self):
        """
        full_match(V,S,T,Ec)
        Fait en gros une petite bdd temporaire
        dico_souche: {'b9':{LEKW00000000.1: [[list_ec_full], [list_ec_part]] ,... }, ...}
        """
        for term in self.result:  # itère les termes
            if term.predicate == "full_match":  # ne retient que les terms full_match !!
                if term.arguments[0] not in self.dico_souche:  # ajout clé vitamine
                    self.dico_souche[term.arguments[0]] = {}  # initialise la cle du dico
                    if term.arguments[1] not in self.dico_souche[term.arguments[0]]:  # si ya pas la clef souche
                        self.dico_souche[term.arguments[0]][term.arguments[1]] = [[term.arguments[3]], []]
                        #                  vitamin              souche             num_ec_full        part_match
                    else:  # si ya la cle de souche
                        self.dico_souche[term.arguments[0]][term.arguments[1]][0] += [term.arguments[3]]
                        #                                                      | pos full

                else:  # si ya la cle vitamine
                    if term.arguments[1] not in self.dico_souche[term.arguments[0]]:  # si ya pas la clef souche
                        self.dico_souche[term.arguments[0]][term.arguments[1]] = [[], [term.arguments[3]]]
                        #                  vitamin              souche                  num_ec_part
                    else:  # si ya la cle de souche
                        self.dico_souche[term.arguments[0]][term.arguments[1]][1] += [term.arguments[3]]


            if term.predicate == "rest_match":
                # todo c'est ici crétin!!
                pass
        print(self.dico_souche)

    def tab_comptage(self, vitamin=None):
        if vitamin is None:
            for key_vit in self.dico_souche.keys():  # itère les vitamines
                for key_souche in self.dico_souche[key_vit].keys():
                    # print(self.dico_souche[key_vit][key_souche])
                    print(key_vit, key_souche)
                    print("Nb_full", len(self.dico_souche[key_vit][key_souche][0]))
                    print("Nb_rest", len(self.dico_souche[key_vit][key_souche][1]))

with open('exemple/ListeAccess', mode='r') as fichaccess:  # ca aussi on sen fout
    listacc = [i.strip() for i in fichaccess]
    inst_resul = Resultats(result, listacc)
    inst_resul.tab_comptage()



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