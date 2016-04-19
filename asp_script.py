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
#     print(termm.arguments)
#     print(termm.predicate)

# Impression du nombre d'élément en sortie
print("Nombre: ", len(result[0]))


class Resultats:

    def __init__(self, m_result, m_list_acc):
        self.result = m_result[0]
        self.list_access = m_list_acc
        self.dico_vit = {}

    def list_ec_vit(self):
        for term in self.result:  # itère les termes
            if term.predicate == "enzymeV":  # ne retient que les terms enzymeV
                # print(term)
                # print(term.arguments[1])
                if term.arguments[0] not in self.dico_vit:  # on ajoute les numéros ec associés à une clé de dico par vit
                    self.dico_vit[term.arguments[0]] = [term.arguments[1]]
                else:
                    self.dico_vit[term.arguments[0]] += [term.arguments[1]]
        print(self.dico_vit)


    def tab_effectifs(self):
        pass



with open('exemple/ListeAccess', mode='r') as fichaccess:
    listacc = [i.strip() for i in fichaccess]
    inst_resul = Resultats(result, listacc)
    inst_resul.list_ec_vit()


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