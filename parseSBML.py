from libsbml import SBMLReader

"""
Les espèces sont dupliquées par compartiments..
Utilise dir() pour trouuver les fonctions
"""

lecteur = SBMLReader()
doc = lecteur.readSBMLFromFile("SBML/subti_folate")
print("Niveau: "+str(doc.getLevel()))


model = doc.getModel()
print("Nombre d'espèces: "+str(model.getNumSpecies()))
print("Nombre de réactions: "+str(model.getNumReactions()))
print(model.getName())
print(model.getNamespaces())
# print(doc.)

listT = []
for i in range(model.getNumSpecies()):

    espece = model.getSpecies(i)
    reaction = model.getReaction(i)

    listT.append(str(espece.getName()))
    # print(espece.getElementName())  # sert un peu a rien, indique le type d'élément..
    # print(espece.getAnnotationString())
    # print(espece.getId)
    # print(reaction.getNotesString())
    # print(reaction.getAnnotationString())

# for i in model.getReactions():
#     print(i)

print(len(set(listT)))
for i in set(listT):
    print(i)