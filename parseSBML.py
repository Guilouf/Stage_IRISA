from libsbml import SBMLReader

lecteur = SBMLReader()
doc = lecteur.readSBMLFromFile("exemple/subti_folate")
model = doc.getModel()
print(model.getNumSpecies())
# print(doc.)



with open("exemple/subti_folate" , 'r') as fich_sbml:
    # document = lecteur.readSBML(fich_sbml)
    # print(fich_sbml.read())
    pass