# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:41:32 2016
Version: 1.0.2 - 20-01-16
@author: Meziane AITE, meziane.aite@inria.fr
"""

#sbmlPlugin

def parseNotes(element):
    notes = element.getNotesString()
    notesList = notes.split("\n")
    notesList = notesList[2:-2]
    notesDict = {}
    for line in notesList:
        start = line.index(">")+1
        end = line.index("<",start)
        line = line[start:end]
        line = line.split(":")
        line[0] = line[0].replace(" ","_")
        line[1] = line[1].replace(" ","")
        line[1] = line[1].replace("|","")
        line[1] = line[1].split(",")
        notesDict[line[0]] = line[1]
    return notesDict

def extractFormula(elementR):
    direction = elementR.getReversible()
    formula = ""
    reactants = (species for species in elementR.getListOfReactants())
    products = (species for species in elementR.getListOfProducts())
    
    species = reactants.next()
    formula = formula + str(species.getStoichiometry()) + " "
    formula = formula + species.getSpecies()
    while True:
        try:
            species = reactants.next()
            formula = formula + " + "+ str(species.getStoichiometry()) + " "
            formula = formula + species.getSpecies()
        except StopIteration:
            if direction:
                formula = formula + " <=> "
            else:
                formula = formula + " => "
            break

    species = products.next()
    formula = formula + str(species.getStoichiometry()) + " "
    formula = formula + species.getSpecies()
    while True:
        try:
            species = products.next()
            formula = formula + " + "+ str(species.getStoichiometry()) + " "
            formula = formula + species.getSpecies()
        except StopIteration:
            break
    return formula

def parseGeneAssoc(GeneAssocStr):
    resultat = GeneAssocStr.replace("(","").replace(")","").replace(" ","").replace("and","or")
    resultat = list(set(resultat.split("or")))
    return resultat

