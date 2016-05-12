from libsbml import SBMLReader
# from libsbml import readSBML  # la diff?
import re
"""
Les espèces sont dupliquées par compartiments..
Utilise dir() pour trouver les fonctions

En gros, les sbml metacyc a disposition:
- On a pas le nom de la souche, à priori un sbml une souche mais bon..

- liste des espèces chimiques:
    - nom, compartiments(duplications..)
    - Notes: leur xrefs

- Liste des réactions:
    - Id, nom, bool reversible
    - Notes: xref et ec number, gene associé
    - Liste des réactans, des produits..
"""

"""
Pour l'instant le but est de traduire les sbml en ASP facon 'ec_uni.lp'
=>
num_access("Souche3","Uni10", "REFSEQ").
uniprot( ec(1,1,1,1),"Uni1").


Après ce serait pas mal de le faire en mode metacyc..
"""


lecteur = SBMLReader()
doc = lecteur.readSBMLFromFile("SBML/subti_folate")
# print("Niveau: "+str(doc.getLevel()))


model = doc.getModel()
# print("Nombre d'espèces: "+str(model.getNumSpecies()))
# print("Nombre de réactions: "+str(model.getNumReactions()))
# print(model.getName())
# print(model.getNamespaces())
# print(doc.)

"""
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
    reaction.notes
    reaction.notes_string

# for i in model.getReactions():
#     print(i)

print(len(set(listT)))
for i in set(listT):
    print(i)
"""

# c'est moche mais au final le plus efficace..
def regex_num_ec(xml):
    num_ec = re.findall('[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,3}\.[0-9]{1,3}', xml)
    return num_ec

# itère les espèces chimiques
# for specie in model.getListOfSpecies():
#     print(specie.getId(), specie.getName())

for reaction in model.getListOfReactions():
    # print(reaction.getId())
    # print(reaction.getNotes())
    # print((dir(reaction)))

    # non callable
    # print(reaction.notes_string)
    # print(reaction.notes)
    # print(dir(reaction.getNotesString()))
    # print(reaction.getNotesString())
    print(regex_num_ec(reaction.getNotesString()))
