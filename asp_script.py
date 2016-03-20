#!/usr/bin/env python
from pyasp.asp import *
from io import StringIO

"""
Memmo base:
is_a(truc,cekilest)
in_pathway(Reaction,Pathway)
ec_number(Reaction,EC)

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


