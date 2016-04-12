#!/usr/bin/env python
from pyasp.asp import *
from io import StringIO

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

for term in result[0]:
    print(term)

# Impression du tableau

print("Nombre: ", len(result[0]))

list_souches = ["LEKW00000000.1", "NZ_CM003439.1", "NZ_CP010528.1", "NZ_CP009236.1", "NC_021514.1", "NC_020229.1",
                "NC_014554.1", "NC_021224.2", "NC_012984.1", "AL935263.2", "FN806773"]

for souche in list_souches:  # parcourt les souches

    if souche not in str(result[0]):
        print("0 ; 0", end='')

    for term in result[0]:  # parcourt les resultats (aléatoire..)
        split_term = str(term).split(",")

        if split_term[1].replace("\"", '') == souche and int(split_term[3][0]) == 4 \
                and split_term[0][0:5] == "statS":
            # print(split_term[1], split_term[2][2:], split_term[3][0], split_term[4][0], end='; ')
            print(split_term[4].replace(')', ''), end=';')

    for term in result[0]:  # parcourt les resultats (aléatoire..)
        split_term = str(term).split(",")

        if split_term[1].replace("\"", '') == souche and int(split_term[3][0]) == 3 \
                and split_term[0][0:5] == "statS":
            # print(split_term[1], split_term[2][2:], split_term[3][0], split_term[4][0], end=' ')
            print(split_term[4].replace(')', ''), end='')

    print('')


