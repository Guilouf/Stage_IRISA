# -*- coding: utf-8 -*-
# coding: utf8
"""
Created on Mon Jul 20 13:03:30 2015
Version: 1.0.2 - 14-01-16
@author: Meziane AITE, meziane.aite@inria.fr

#Todo what if stochio = n ?
#metacyc to sbml: ne pas utiliser suppData. species = node if node dans rlt consumes/produces.

"""
from tinygraphdbplus import Tinygraphdbplus
from tinygraphdb import Tinygraphdb
try:
    from libsbml import *
except:
    print("package libsbml needed, use this cmd:\n pip install "
          + "python-libsbml")
    exit()
import re

def check(value, message):
    """If 'value' is None, prints an error message constructed using
    'message' and then exits with status code 1.  If 'value' is an integer,
    it assumes it is a libSBML return status code.  If the code value is
    LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
    prints an error message constructed using 'message' along with text from
    libSBML explaining the meaning of the code, and exits with status code 1.
    """
    if value == None:
        raise SystemExit('LibSBML returned a null value trying to ' + message + '.')
    elif type(value) is int:
        if value == LIBSBML_OPERATION_SUCCESS:
            return
        else:
            err_msg = 'Error encountered trying to ' + message + '.' \
                 + 'LibSBML returned error code ' + str(value) + ': "' \
                 + OperationReturnValue_toString(value).strip() + '"'
            raise SystemExit(err_msg)
    else:
        return

    
def tgdbp_to_basic_SBML(tgdbp_file_name, sbml_lvl = 2, sbml_version = 1):
    """
    #basic without compartment, cell by default
    #metacyc specific
    """
    #create a sbml model empty
    document = SBMLDocument(sbml_lvl, sbml_version)
    model = document.createModel()
    compart = model.createCompartment()
    check(compart,'create compartment')
    check(compart.setId('cell'),'set compartment id')        
    
    #load tgdbp
    tgdbp = Tinygraphdbplus(tgdbp_file_name)
    
    #generator of nodes that have suppData, 
    hasSuppDataNodes = [tgdbp.getDicOfNode()[rlt.getIdIn()] for rlt in tgdbp.getTuplOfRelation() if rlt.getType() == "has suppData"]
    species = ((n.getId(),n.getMisc()["metacyc_id"][0]) for n in hasSuppDataNodes if n.getClass() != "reaction")
    reactions = ((k,n.getMisc()["metacyc_id"][0]) for k,n in tgdbp.getDicOfNode().iteritems() if n.getClass() == "reaction")

    for (sId,sName) in species:
        s = model.createSpecies()
        check(s, 'create species s1')
        check(s.setId(sId), 'set species s1 id')
        check(s.setName(sName), 'set species s1 id')
        check(s.setCompartment('cell'), 'set species s1 compartment')
     
    # Create a reaction inside this model, set the reactants and products,
    # and set the reaction rate expression (the SBML "kinetic law").  We
    # set the minimum required attributes for all of these objects.  The
    # units of the reaction rate are determined from the 'timeUnits' and
    # 'extentUnits' attributes on the Model object.
    for rId,rName in reactions:
        consumes = ((rlt.getIdOut(),rlt.getMisc()["stoichiometry"][0]) for rlt in tgdbp.getRelation(rId,"in") if rlt.getType() == "consumes")
        produces = ((rlt.getIdOut(),rlt.getMisc()["stoichiometry"][0]) for rlt in tgdbp.getRelation(rId,"in") if rlt.getType() == "produces")
        try:
            direction = tgdbp.getDicOfNode()[rId].getMisc()["direction"][0]
            if direction == "LEFT-TO-RIGHT":
                reversible = False
            else:
                reversible = True
        except KeyError:
            reversible = False
        r = model.createReaction()
        check(r, 'create reaction')
        check(r.setId(rId), 'set reaction id')
        check(r.setName(rName), 'set species s1 id')
        check(r.setReversible(reversible), 'set reaction reversibility flag')
        
        for cId,stoich in consumes:
            try:
                stoich = int(stoich)
            except ValueError:
                stoich = 1
            species_ref = r.createReactant()
            check(species_ref, 'create reactant')
            check(species_ref.setSpecies(prefix+cId), 'assign reactant species')
            check(species_ref.setStoichiometry(stoich), 'set stoichiometry')

        for pId,stoich in produces:
            try:
                stoich = int(stoich)
            except ValueError:
                stoich = 1
            species_ref = r.createProduct()
            check(species_ref, 'create product')
            check(species_ref.setSpecies(prefix+pId), 'assign product species')
            check(species_ref.setStoichiometry(stoich), 'set stoichiometry')
       
    return (document,tgdbp)        

        
def tgdbp_to_SBML_for_meneco(tgdbp_file_name, sbml_file_name, prefix, sbml_lvl = 2, sbml_version = 1):
    (document,tgdbp) = tgdbp_to_basic_SBML(tgdbp_file_name, prefix, sbml_lvl, sbml_version)
    return writeSBMLToFile(document, sbml_file_name)


def tgdbp_to_SBML_for_shogen(tgdbp_file_name, sbml_file_name, prefix, sbml_lvl = 2, sbml_version = 1):
    (document,tgdbp) = tgdbp_to_basic_SBML(tgdbp_file_name, prefix, sbml_lvl, sbml_version)
    model = document.getModel()
    listOfReactions = model.getListOfReactions()

    
    for r in listOfReactions:
        rNode = tgdbp.getNode(r.getName(),"metacyc_id",True)
        if rNode is not None:
            rNode = rNode[0][1]
            suppData = (tgdbp.getDicOfNode()[rlt.getIdOut()] 
            for rlt in tgdbp.getRelation(rNode.getId(),"in") 
            if rlt.getType() == "has suppData")
            setOfGene = set()
            try:
                for n in suppData:
                    if "GENE_ASSOCIATION" in n.getMisc().keys():
                        genes = n.getMisc()["GENE_ASSOCIATION"][0]
                        for ch in ["(",")"," "]:
                            if ch in genes:
                                genes = genes.replace(ch,"")
                        genes = genes.replace("and","or")
                        genes = genes.split("or")
                        for g in genes:
                            setOfGene.add(g)
            except:
                pass
            
            if len(setOfGene) != 0:
                gene_assoc = ""
                count = 0
                for g in setOfGene:
                    count += 1
                    if count == len(setOfGene):
                        gene_assoc += g
                    else:
                        gene_assoc += g +" or "
                notes = "<html:body><html:p>"
                notes += "GENE_ASSOCATION:" + gene_assoc
                notes += "</html:p></html:body>"
                r.setNotes(notes)
        else:
            print(r+" not found in tgdbRef")
    return writeSBMLToFile(document,sbml_file_name)    

def tgdbp_to_SBML_for_FBA(tgdbp_file_name, sbml_file_name, prefix, sbml_lvl = 2, sbml_version = 1):
    (document,tgdbp) = tgdbp_to_basic_SBML(tgdbp_file_name, prefix, sbml_lvl, sbml_version)
    model = document.getModel()
    listOfReactions = model.getListOfReactions()

    
    for r in listOfReactions:
        rNode = tgdbp.getNode(r.getName(),"metacyc_id",True)
        if rNode is not None:
            rNode = rNode[0][1]
            suppData = (tgdbp.getDicOfNode()[rlt.getIdOut()] 
            for rlt in tgdbp.getRelation(rNode.getId(),"in") 
            if rlt.getType() == "has suppData")
            setOfGene = set()
            try:
                for n in suppData:
                    if "GENE_ASSOCIATION" in n.getMisc().keys():
                        genes = n.getMisc()["GENE_ASSOCIATION"][0]
                        for ch in ["(",")"," "]:
                            if ch in genes:
                                genes = genes.replace(ch,"")
                        genes = genes.replace("and","or")
                        genes = genes.split("or")
                        for g in genes:
                            setOfGene.add(g)
            except:
                pass
            
            if len(setOfGene) != 0:
                gene_assoc = ""
                count = 0
                for g in setOfGene:
                    count += 1
                    if count == len(setOfGene):
                        gene_assoc += g
                    else:
                        gene_assoc += g +" or "
                notes = "<html:body><html:p>"
                notes += "GENE_ASSOCATION:" + gene_assoc
                notes += "</html:p></html:body>"
                r.setNotes(notes)
        else:
            print(r+" not found in tgdbRef")
    return writeSBMLToFile(document,sbml_file_name)     

#################################

def tgdb_to_basic_SBML(tgdb_file_name, sbml_lvl = 2, sbml_version = 1):
    """
    #basic without compartment, cell by default
    #metacyc specific
    """
    #create a sbml model empty
    document = SBMLDocument(sbml_lvl, sbml_version)
    model = document.createModel()
    compart = model.createCompartment()
    check(compart,'create compartment')
    check(compart.setId('cell'),'set compartment id')        
    
    #load tgdbp
    tgdb = Tinygraphdb(tgdb_file_name)
    
    #generator of nodes that have suppData,
    speciesID = set([rlt.getIdOut() for rlt in tgdb.getTuplOfRelation() 
    if rlt.getType() == "consumes"
    or rlt.getType() == "produces"])
    species = ((_id,tgdb.getDicOfNode()[_id].getMisc()["metacyc_id"][0]) for _id in speciesID)
    reactions = ((k,n.getMisc()["metacyc_id"][0]) for k,n in tgdb.getDicOfNode().iteritems() if n.getClass() == "reaction")
    
    print("species")
    for (sId,sName) in species:
        #print(sId)
        s = model.createSpecies()
        check(s, 'create species s1')
        check(s.setId(sId), 'set species s1 id')
        check(s.setName(sName), 'set species s1 id')
        check(s.setCompartment('cell'), 'set species s1 compartment')
     
    # Create a reaction inside this model, set the reactants and products,
    # and set the reaction rate expression (the SBML "kinetic law").  We
    # set the minimum required attributes for all of these objects.  The
    # units of the reaction rate are determined from the 'timeUnits' and
    # 'extentUnits' attributes on the Model object.
    print("reaction")
    for rId,rName in reactions:
        #print(rId)
        consumes = ((rlt.getIdOut(),rlt.getMisc()["stoichiometry"][0]) for rlt in tgdb.getRelation(rId,"in") if rlt.getType() == "consumes")
        produces = ((rlt.getIdOut(),rlt.getMisc()["stoichiometry"][0]) for rlt in tgdb.getRelation(rId,"in") if rlt.getType() == "produces")
        try:
            direction = tgdb.getDicOfNode()[rId].getMisc()["direction"][0]
            if direction == "LEFT-TO-RIGHT":
                reversible = False
            else:
                reversible = True
        except KeyError:
            reversible = False
        r = model.createReaction()
        check(r, 'create reaction')
        check(r.setId(rId), 'set reaction id')
        check(r.setName(rName), 'set species s1 id')
        check(r.setReversible(reversible), 'set reaction reversibility flag')
        
        for cId,stoich in consumes:
            try:
                stoich = int(stoich)
            except ValueError:
                stoich = 1
            species_ref = r.createReactant()
            check(species_ref, 'create reactant')
            check(species_ref.setSpecies(cId), 'assign reactant species')
            check(species_ref.setStoichiometry(stoich), 'set stoichiometry')

        for pId,stoich in produces:
            try:
                stoich = int(stoich)
            except ValueError:
                stoich = 1
            species_ref = r.createProduct()
            check(species_ref, 'create product')
            check(species_ref.setSpecies(pId), 'assign product species')
            check(species_ref.setStoichiometry(stoich), 'set stoichiometry')
       
    return (document,tgdb)

def tgdb_to_SBML_for_meneco(tgdb_file_name, sbml_file_name, sbml_lvl = 2, sbml_version = 1):
    (document,tgdb) = tgdb_to_basic_SBML(tgdb_file_name, sbml_lvl, sbml_version)
    return writeSBMLToFile(document, sbml_file_name)
