from libsbml import SBMLReader
# from libsbml import readSBML  # la diff?
from lxml import *
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

# todo ne pas se faire chier et faire une regex sur le xml..

# import xmltodict # pas l'air mal.;
import xml.etree.ElementTree
# e = xml.etree.ElementTree.parse('thefile.xml').getroot()

from io import StringIO

def get_ec_num2(xml):
    xmlIO = StringIO(xml)
    e = xml.etree.ElementTree.parse(xmlIO).getroot()



def get_ec_num(xml):
    dico = xml.__dict__
    # print(dico['notes'])
    clef = [cle for cle in dico.keys()]
    # print(clef)
    # print(dico['this'])

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
    print(reaction.getNotesString())
    # get_ec_num(reaction.getNotesString())
    # get_ec_num(reaction.notes)

    # e = xml.etree.ElementTree.parse().getroot()
    get_ec_num2(reaction.getNotesString())











#      Code lucas
# -*- coding: utf-8 -*-
"""
definition of the SBML input format converter.
The data is used as follow:
    - species are nodes;
    - reactions are nodes;
    - an edge is created between each reaction node and each species involved in it;
"""

import itertools

# from powergrasp import commons
# from powergrasp.converter.input_converter import InConverter

# LOGGER = commons.logger()
# NAME_PREFIX = 'metacyc:'
#
#
# class InSBML(InConverter):
#     """Convert given SBML file in ASP file"""
#     FORMAT_NAME = 'sbml'
#     FORMAT_EXTENSIONS = ('sbml',)
#
#     def _gen_edges(self, filename_sbml:str) -> dict:
#         """Yields pair (node, successor), representing the data contained
#         in input sbml file.
#         """
#         try:
#             yield from sbml_to_atom_generator(filename_sbml)
#         except IOError as e:
#             LOGGER.error(self.error_input_file(filename_sbml, e))
#         except ImportError:
#             LOGGER.error("libsbml module is necessary for use SBML as input"
#                          " format. 'pip install libsbml' should do the job."
#                          " Compression aborted.")
#             exit(1)
#         return  # empty generator pattern
#         yield
#
#
# def sbml_to_atom_generator(filename:str) -> dict:
#     from libsbml import readSBML
#
#     document = readSBML(filename)
#     level    = document.getLevel()
#     version  = document.getVersion()
#     model    = document.getModel()
#
#     LOGGER.info('libsbml found a SBML data of level ' + str(level)
#                 + ' and of version ' + str(version) + '.')
#
#     # print lib fatal error of the libsbml
#     errors = (document.getError(idx) for idx in itertools.count())
#     errors = (err for err in itertools.takewhile(lambda e: e is not None, errors)
#               if err.isError() or err.isFatal())
#     for error in errors:
#         LOGGER.error('libsbml error on input file: ' + error.getMessage().strip())
#
#     if (model == None):
#         LOGGER.error('libsbml: No model found in file ' + filename + '.' )
#         exit(1)
#
#     # build dictionnary that link species id with its name
#     species_name = {}
#     for specie in model.getListOfSpecies():
#         species_name[specie.getId()] = specie.getName().lstrip(NAME_PREFIX)
#
#     # get reactions, produces all edges in the outputed dict
#     for reaction in model.getListOfReactions():
#         name = reaction.getName().lstrip(NAME_PREFIX)
#         products  = (species_name[p.getSpecies()] for p in reaction.getListOfProducts() )
#         reactants = (species_name[p.getSpecies()] for p in reaction.getListOfReactants())
#         for node in itertools.chain(products, reactants):
#             yield name, node
