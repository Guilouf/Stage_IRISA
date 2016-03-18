#!/usr/bin/env python
from pyasp.asp import *

goptions = ''  # soluce max gringo
soptions = ''  # solutions max solveur
solver = Gringo4Clasp(gringo_options=goptions, clasp_options=soptions)

# Liste des fichiers asp
hidden = 'ASP/hidden.lp'
base = 'ASP/metacyc_18.5.lp'
query = 'ASP/explore.lp'
# Solver
result = solver.run([hidden, base, query], collapseTerms=True, collapseAtoms=False)

for term in result[0]:
    print(term)
