# -*- coding: utf-8 -*-
# coding: utf8
"""
Created on Mon Jul 20 13:03:30 2015
Version: 1.0.2 - 20-01-16
@author: Meziane AITE, meziane.aite@inria.fr

Contains all necessary function to generate wikiPages from a tgdbp and update 
a wiki online require WikiManger module (with wikiMate,Vendor)

# TODO: ameliorer l'update avec wikimate de facon a ne pas avoir a se log 
# a chaque fois pour envoyer une page ou utiliser en multiP, 4 bots pour 
# envoyer les pages.
#TODO !! UPDATE
"""

import parameters as para
from multiprocessing import Pool, cpu_count
import os
import shutil

def tgdbpToWiki(localTgdbRef, localNewTgdbp,
                localOldTgdbp = None, updateWiki = False):
    """
    Main function to generete wikiPages and Update the wiki online
    If oldTgdb is None, the function will create all the wiki page of the 
    network and upload them to the wiki else, it will delete all the obsolete
    page from the wiki, then create all the wiki page of the new network.
    
    input:  localTgdbRef: <TGDB> Tinygraphdb of metacyc
            localNewTgdbp: <TGDBP> Tinygraphdbplus of the new or current network
            localOldTgdbp <TGDBP> Tinygraphdbplus of the old version if exist
    output: file .txt which contains the wikicode to create pages
    #TODO UPDATE !!
    """
    #need to convert to global var for multi processing
    global tgdbRef,newTgdbp,oldTgbdp
    tgdbRef,newTgdbp = localTgdbRef,localNewTgdbp
    if localOldTgdbp is None:
        oldTgdbp = None
    else:
        oldTgdbp = localOldTgdbp

    # create all the directory required
    print("Creating directory...\n")
    createDirectory()

    # def the reactions, metabolites, pathways and genes
    print("Loading all entry ...\n")
    tmpNewReactions = (k for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "reaction" )
    tmpNewMetabolites = set()
    print("\tMetabolites...\n")
    for k in tmpNewReactions:
        relations = (rlt.getIdOut() for rlt in newTgdbp.getRelation(k,"in") if 
         rlt.getType() == "has left"
         or rlt.getType() == "has right")
        for _id in relations:
            tmpNewMetabolites.add(_id)
    nbMetabolites = len(tmpNewMetabolites)
    newMetabolites = ((k,newTgdbp.getDicOfNode()[k].getMisc()["metacyc_id"][0]) for k in tmpNewMetabolites)
    print("Done, "+str(nbMetabolites)+" Metabolites wikiPages to create\n")
    
    print("\tGenes...\n")
    newGenes = ((k,n.getMisc()["metacyc_id"][0]) for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "gene" )
    nbGenes = 0
    for G in newGenes:
        nbGenes += 1
    newGenes = ((k,n.getMisc()["metacyc_id"][0]) for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "gene" )
    print("Done, "+str(nbGenes)+" Genes wikiPages to create\n")

    print("\tPathways...\n")
    newPathways = ((k,n.getMisc()["metacyc_id"][0]) for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "pathway" )
    nbPathways = 0
    for P in newPathways:
        nbPathways += 1
    newPathways = ((k,n.getMisc()["metacyc_id"][0]) for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "pathway" )
    print("Done, "+str(nbPathways)+" Pathways wikiPages to create\n")

    print("\tReactions...\n")
    newReactions = ((k,n.getMisc()["metacyc_id"][0]) for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "reaction" )
    nbReactions = 0
    for R in newReactions:
        nbReactions += 1
    newReactions = ((k,n.getMisc()["metacyc_id"][0]) for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "reaction" )
    print("Done, "+str(nbReactions)+" Reactions wikiPages to create\n")
    #create all wiki pages
    #Genes
    print("Starting multiprocessing wikiPage Generation...")
    p = Pool(processes=cpu_count())
    for nbEntry,entryGenerator,entryFunction in [(nbMetabolites,newMetabolites,mp_createWikiPageMetabolite),(nbGenes,newGenes,mp_createWikiPageGene),(nbPathways,newPathways,mp_createWikiPagePathway),(nbReactions,newReactions,mp_createWikiPageReaction)]:
        cSize = int(nbEntry/cpu_count())+1
        resultats = p.imap(entryFunction, entryGenerator, chunksize = cSize)
        [None for _ in resultats]
    print("wikiPages successfuly created\n")        
    if updateWiki:
        #compare old vs new:
        if oldTgdbp is None:
            #Just send all the wikiPages
            wikiUpdate(para.path_Resultats)        
        else:
            # Delete obsolete pages from wiki then send all the WikiPages
            allMetacycId2Delete = compareTgdbp(newTgdbp,oldTgdbp)
            wikiUpdate(para.path_Resultats,allMetacycId2Delete)
    #in case we just want the wikipages
    else:
        print("The wiki will not been updated. Only wikiPages created.")

def createDirectory(dirPath = para.path_Resultats):
    """
    create the folders genes, reactions, metabolites, pathways in the folder resultats/
    if already exist, it will replace old folders (and delete old files)
    """
    dirNames = ["genes","reactions","metabolites","pathways"]
    #creatings the directory which will contains the wiki pages
    for d in dirNames:
        if not os.path.exists(dirPath+d):
            os.makedirs(dirPath+d)
        else:
            print("The directory "+dirPath+d+" containing wikiPage already exist. Old pages will be deleted !!")
            shutil.rmtree(dirPath+d)
            os.makedirs(dirPath+d)

def compareTgdbp(newTgdbp,oldTgdbp):
    """
    recover all the metabolites, genes pathways and reactions of two given network and return
    a list of metacyc_id deleted from the old to the new version
    input:  newTgdbp: <TGDBP> Tinygraphdbplus of the new or current network
            oldTgdbp <TGDBP> Tinygraphdbplus of the old version if exist
    output: allMetacycId2Delete <set> set of metacyc_id corresponding to wiki page name to delete
    """
    setNewMetabolites = set()
    setNewGenes = set()
    setNewPathways = set()
    setNewReactions = set()

    setOldMetabolites = set()
    setOldGenes = set()
    setOldPathways = set()
    setOldReactions = set()

    tmpNewReactions = (k for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "reaction" )
    for k in tmpNewReactions:
        relations = (rlt.getIdOut() for rlt in newTgdbp.getRelation(k,"in") if 
         rlt.getType() == "has left"
         or rlt.getType() == "has right")
        for _id in relations:
            setNewMetabolites.add(_id)
    newGenes = (k for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "gene" )
    for G in newGenes:
        setNewGenes.add(G)
    newPathways = (k for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "pathway" )
    for P in newPathways:
        setNewPathways.add(P)
    newReactions = (k for (k,n) in newTgdbp.getDicOfNode().iteritems() if n.getClass() == "reaction" )
    for R in newReactions:
        setNewReactions.add(R)

    #Get Old entry        
    tmpOldReactions = (k for (k,n) in oldTgdbp.getDicOfNode().iteritems() if n.getClass() == "reaction" )
    for k in tmpOldReactions:
        relations = (rlt.getIdOut() for rlt in oldTgdbp.getRelation(k,"in") if 
         rlt.getType() == "has left"
         or rlt.getType() == "has right")
        for _id in relations:
            setOldMetabolites.add(_id)
    oldGenes = (k for (k,n) in oldTgdbp.getDicOfNode().iteritems() if n.getClass() == "gene" )
    for G in oldGenes:
        setOldGenes.add(G)
    oldPathways = (k for (k,n) in oldTgdbp.getDicOfNode().iteritems() if n.getClass() == "pathway" )
    for P in oldPathways:
        setOldPathways.add(P)
    oldReactions = (k for (k,n) in oldTgdbp.getDicOfNode().iteritems() if n.getClass() == "reaction" )
    for R in oldReactions:
        setOldReactions.add(R)
    
    # Set of metacyc_id to delete.
    reactions2delete = setOldReactions.difference(setNewReactions)
    genes2delete = setOldGenes.difference(setNewGenes)
    pathways2delete = setOldPathways.difference(setNewPathways)
    metabolites2delete = setOldMetabolites.difference(setNewMetabolites)
    allId2Delete = reactions2delete.union(genes2delete).union(pathways2delete).union(metabolites2delete)
    allMetacycId2Delete = set()
    for _id in allId2Delete:
        metacycID = oldTgdbp.getDicOfNode()[_id].getMisc()["metacyc_id"][0]
        allMetacycId2Delete.add(metacycID)

    return(allMetacycId2Delete)

def mp_createWikiPageGene(tuplId):
    """
    multiProcessing version of the function.
    input: tuplId: <tuple>  tuplId[0]: <int> unique_id access
                            tuplId[1]: <string> metacyc_id access
    output: pageInArray <List>: corresponding to the wikiPage
    """
    pageInArray = createWikiPageGene(tgdbRef,newTgdbp,tuplId[0],"id")
    fileName = para.path_Resultats+"genes/"+tuplId[1]+".txt"
    createWikiFile(pageInArray,fileName)

    
def createWikiPageGene(tgdbRef,tgdbp,_arg,_type):
    """
    create a file with all the wikicode to create the page of the given Gene
    input:  tgdbRef: <TGDB>: tgdb of reference.
            tgdbp: <TGDBP> : tgdbplus of the current network
            _arg: <string>: node acces (id,metacyc_id,common_name)
            _type: <string>: refere to the _arg (id,metacyc,cname)
            
    output: list pageinArray
    """
    try:
        nodeId,node = tgdbp.getNodeId(_arg,_type,True)[0]
        nodeClass = node.getClass()
        if nodeClass != "gene":
            raise TypeError("The given arguments don't refer to a gene")
    except TypeError:
        print("Unable to find the node with given arguments")
        return False
    
    # Recover all associations
    reactionAssoc = (tgdbp.getDicOfNode()[rlt.getIdIn()] for rlt in tgdbp.getRelation(nodeId,"out")
     if rlt.getType() == "is linked to")
    proteinAssoc = (tgdbp.getDicOfNode()[rlt.getIdOut()] for rlt in tgdbp.getRelation(nodeId,"in")
     if rlt.getType() == "codes for")

    with open(para.gene_template) as f:
        pageInArray = f.readlines()
    #2nd line is where the gene name is defined
    pageInArray[1] = pageInArray[1].replace("gene_name",node.getMisc()["origin_id"][0])
    # create dictionary for each kind of assignment
    allAsso = {"AUTOMATED-NAME-MATCH":[], "EC-NUMBER":[], "FUNCTIONAL":[],
               "GO-TERM":[], "ORTHO_AT_SILICO":[], "ORTHO_AT_EXP":[],
               "MANUAL":[],"UNKNOWN":[]}
    
    Try:
        for Rnode in reactionAssoc:
            # Recover the DB_id of reactions associated with the current gene
            reaction_name = tgdbp.getDicOfNode()[rlt.getIdOut()].getMisc()["metacyc_id"][0]
            allAsso[rlt.getMisc()["assignment"]].append(reaction_name)
    #iteritems on the dico allAsso, k: type of assignment, n: liste of reactions name
    for iteri in allAsso.iteritems():
        if iteri[0] == "AUTOMATED-NAME-MATCH" and len(iteri[1]) != 0:
            pageInArray.append("* Functional description (Pathway Tools)\n")
            for Rname in iteri[1]:
                pageInArray.append("** [[associated to reaction::"+Rname+"]]\n")
        elif iteri[0] == "EC-NUMBER" and len(iteri[1]) != 0:
            pageInArray.append("* EC number (Pathway Tools)\n")
            for Rname in iteri[1]:
                pageInArray.append("** [[associated to reaction::"+Rname+"]]\n")
        elif iteri[0] == "FUNCTIONAL" and len(iteri[1]) != 0:
            pass
        elif iteri[0] == "GO-TERM" and len(iteri[1]) != 0:
            pageInArray.append("* Gene Ontology Term (Pathway Tools)\n")
            for Rname in iteri[1]:
                pageInArray.append("** [[associated to reaction::"+Rname+"]]\n")
        elif iteri[0] == "ORTHO_AT_SILICO" and len(iteri[1]) != 0:
            pageInArray.append("* ORTHO_AT_SILICO\n")
            for Rname in iteri[1]:
                pageInArray.append("** [[associated to reaction::"+Rname+"]]\n")
        elif iteri[0] == "ORTHO_AT_EXP" and len(iteri[1]) != 0:
            pageInArray.append("* ORTHO_AT_EXP\n")
            for Rname in iteri[1]:
                pageInArray.append("** [[associated to reaction::"+Rname+"]]\n")
        elif iteri[0] == "MANUAL" and len(iteri[1]) != 0:
            pageInArray.append("* MANUAL\n")
            for Rname in iteri[1]:
                pageInArray.append("** [[associated to reaction::"+Rname+"]]\n")
        elif iteri[0] not in allAsso.keys():
            print(iteri[0])
            print(iteri[1])
            raise KeyError("Unknown Association")
    return(pageInArray)

def mp_createWikiPageReaction(tuplId):
    """
    multiProcessing version of the function.
    input: tuplId: <tuple>  tuplId[0]: <int> unique_id access
                            tuplId[1]: <string> metacyc_id access
    output: pageInArray <List>: corresponding to the wikiPage
    """
    pageInArray = createWikiPageReaction(tgdbRef,newTgdbp,tuplId[0],"id")
    fileName = para.path_Resultats+"reactions/"+tuplId[1]+".txt"
    createWikiFile(pageInArray,fileName)

def createWikiPageReaction(tgdbRef,tgdbp,_arg,_type):
    """
    create a file with all the wikicode to create the page of the given Reaction
    input:  tgdbRef: <TGDB>: tgdb of metacyc
            tgdbp: <TGDBP> : tgdbplus of the current network
            _arg: <string>: node acces (unique_id,metacyc_id,common_name)
            _type: <string>: refere to the node acess (id,metacyc,cname)
    output: list pageinArray
    """
    try:
        nodeId,node = tgdbp.getNodeId(_arg,_type)
        _class = node.getClass()
        if _class != "reaction":
            raise TypeError
    except TypeError:
        print("Unable to find the node with given arguments")
        return False

    RmetacycID = node.getMisc()["metacyc_id"][0]
    with open(para.reaction_template) as f:
        pageInArray = f.readlines()
    #2nd line is where the reaction name is defined
    #if from metacyc, then use hyperlink to metacyc.org
    if "Manual" not in RmetacycID:
        pageInArray[1] = pageInArray[1].replace("reaction_metacycID",RmetacycID)
    #in case of reaction added manually, do not use the metacyc link
    else:
        pageInArray[1] = "== Reaction "+RmetacycID+" == {{#set:metacyc id="+RmetacycID+"}}\n"
    #check if common name associated
    if "common_name" in node.getMisc().keys():
        i = pageInArray.index("* Common name:\n")+1
        for cname in node.getMisc()["common_name"]:
            pageInArray.insert(i,"** "+cname+"{{#set:name="+cname+"}}\n")
            i += 1
    #check if ec number associated
    if "ec" in node.getMisc().keys():
        ec = node.getMisc()["ec"][0]
        ec = ec.replace("EC-","")
        i = pageInArray.index("* EC number:\n")
        pageInArray[i] = "EC number: [http://enzyme.expasy.org/EC/"+ec+" "+ec+"]{{#set:ec-number="+ec+"}}\n"
    #check synonymous ('has name' relations) / generator of 'has name' relations
    names = [rlt for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "has name"]
    if len(names) != 0:
        i = pageInArray.index("* Synonyms:\n")+1
        for synRLT in names:
            syn = tgdbp.getDicOfNode()[synRLT.getIdOut()].getMisc()["label"][0]
            pageInArray.insert(i,"** "+syn+"{{#set:name="+syn+"}}\n")
            i += 1
    #check if hmm association
    i = pageInArray.index("* HMM model:\n")
    try:
        HMM = [rlt for rlt in tgdbp.getRelation(nodeId,"out") if rlt.getType() == "catalyses"]
        pageInArray[i] = "* HMM model: Yes\n"
    except TypeError:
        pageInArray[i] = "* HMM model: No\n"
        HMM = None
    # define the formula, metacyc version and common name version
    formulaLeft = ((rlt.getIdOut(),rlt.getMisc()["stoichiometry"][0]) for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "has left")
    formulaRight = ((rlt.getIdOut(),rlt.getMisc()["stoichiometry"][0]) for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "has right")
    #recovering left compounds
    LformulaMetacyc = []
    LformulaCname = []
    for left in formulaLeft:
        compoundMetacycId = tgdbp.getDicOfNode()[left[0]].getMisc()["metacyc_id"][0]
        #if metabolite have common name, recovere it, else, just use the metacyc_id
        try:
            compoundCommonName = tgdbp.getDicOfNode()[left[0]].getMisc()["common_name"][0]
        except KeyError:
            compoundCommonName = tgdbp.getDicOfNode()[left[0]].getMisc()["metacyc_id"][0]
        #append in list, tuple of stoichio and metacycID / commoname
        LformulaMetacyc.append(str(left[1]+" [["+compoundMetacycId+"]]"))
        LformulaCname.append(str(left[1]+" "+compoundCommonName))
    formulaMetacycId = " '''+''' ".join(LformulaMetacyc)
    formulaCname = " '''+''' ".join(LformulaCname)
    try:
        if node.getMisc()["direction"][0] == "LEFT-TO-RIGHT":
            formulaMetacycId = formulaMetacycId + " '''=>''' "
            formulaCname = formulaCname + " '''=>''' "
        elif node.getMisc()["direction"][0] == "RIGHT-TO-LEFT":
            formulaMetacycId = formulaMetacycId + " '''<=''' "
            formulaCname = formulaCname + " '''<=''' "
        elif node.getMisc()["direction"][0] == "REVERSIBLE":
            formulaMetacycId = formulaMetacycId + " '''<=>''' "
            formulaCname = formulaCname + " '''<=>''' "
    except KeyError:
            formulaMetacycId = formulaMetacycId + " '''<=>''' "
            formulaCname = formulaCname + " '''<=>''' "
    #recovering right compounds
    RformulaMetacyc = []
    RformulaCname = []
    for right in formulaRight:
        compoundMetacycId = tgdbp.getDicOfNode()[right[0]].getMisc()["metacyc_id"][0]
        try:
            compoundCommonName = tgdbp.getDicOfNode()[right[0]].getMisc()["common_name"][0]
        except KeyError:
            compoundCommonName = tgdbp.getDicOfNode()[right[0]].getMisc()["metacyc_id"][0]
        RformulaMetacyc.append(str(right[1]+" [["+compoundMetacycId+"]]"))
        RformulaCname.append(str(right[1]+" "+compoundCommonName))
    formulaMetacycId = formulaMetacycId + " '''+''' ".join(RformulaMetacyc)+"\n"
    formulaCname = formulaCname + " '''+''' ".join(RformulaCname)+"\n"
    i = pageInArray.index("reaction_formulaMetacyc\n")
    pageInArray[i] = pageInArray[i].replace("reaction_formulaMetacyc\n",formulaMetacycId)
    i = pageInArray.index("reaction_formulaCname\n")
    pageInArray[i] = pageInArray[i].replace("reaction_formulaCname\n",formulaCname)
    #check if compartment associated
    if "compartment" in node.getMisc().keys():
        i = pageInArray.index("== Predicted compartment(s) ==\n")+1
        for compart in node.getMisc()["compartment"]:
            pageInArray.insert(i,"* "+compart+"\n")
            i += 1
    #recovere pathways associated
    i = pageInArray.index("== Pathways ==\n")+1
    pathways = (tgdbp.getDicOfNode()[rlt.getIdOut()] for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "is in pathway" )
    for p in pathways:
        #recovere from metacyc, the nb of reactions associated to the pathway
        nbReactionsTotal = len([rlt for rlt in tgdbRef.getRelation(p.getId(),"out") if rlt.getType() == "is in pathway"])
        nbReactionsFound = len([rlt for rlt in tgdbp.getRelation(p.getId(),"out") if rlt.getType() == "is in pathway"])
        pageInArray.insert(i,"{{#set:is in pathway="+p.getMisc()["metacyc_id"][0]+"}}\n")
        i += 1
        #try in case no common_name for the pathway, (its possible in metacyc)
        try:
            pageInArray.insert(i,"* [["+p.getMisc()["metacyc_id"][0]+"]]: "+p.getMisc()["common_name"][0]+", [http://metacyc.org/META/NEW-IMAGE?object="+p.getMisc()["metacyc_id"][0]+" view in MetaCyc]\n")
        except KeyError:
            pageInArray.insert(i,"* [["+p.getMisc()["metacyc_id"][0]+"]]: "+p.getMisc()["metacyc_id"][0]+", [http://metacyc.org/META/NEW-IMAGE?object="+p.getMisc()["metacyc_id"][0]+" view in MetaCyc]\n")
        i += 1
        pageInArray.insert(i,"** "+str(nbReactionsFound)+" reactions found in ''"+para.fullSpeciesName+"'' over "+str(nbReactionsTotal)+" reactions in the full pathway as defined in MetaCyc\n")
        i += 1
    #recovere genes associated 
    i = pageInArray.index("== ''fullSpeciesName'' genes associated with this reaction  ==\n")
    pageInArray[i] = pageInArray[i].replace("fullSpeciesName",para.fullSpeciesName)
    i += 1
    pageInArray[i] = pageInArray[i].replace("fullSpeciesName",para.fullSpeciesName)
    i += 1
    #list of tuple (gene ID,type of assignment)
    try:
        assignments = ((rlt.getIdIn(),rlt.getMisc()["assignment"]) for rlt in tgdbp.getRelation(nodeId,"out") if rlt.getType() == "is associated with")
        # Regroup all assignments in a dictionnary, key = type of assignment,
        # value = list of gene's fake metacyc_id                
        allAsso = {"AUTOMATED-NAME-MATCH":[], "EC-NUMBER":[], "FUNCTIONAL":[],
                   "GO-TERM":[], "ORTHO_AT_SILICO":[], "ORTHO_AT_EXP":[],
                   "MANUAL":[]}

        for _tuple in assignments:
            allAsso[_tuple[1]].append(tgdbp.getDicOfNode()[_tuple[0]].getMisc()["metacyc_id"][0])
        for iteri in allAsso.iteritems():
            if iteri[0] == "AUTOMATED-NAME-MATCH" and len(iteri[1]) != 0:
                pageInArray.insert(i,"* '''Functional description (Pathway Tools)'''{{#set:evidence=AUTOMATED-NAME-MATCH}}\n")
                i += 1
                for Gname in iteri[1]:
                    pageInArray.insert(i,"** [["+Gname+"]] {{#set:gene association="+Gname+" (AUTOMATED-NAME-MATCH)}}\n")
                    i += 1
            elif iteri[0] == "EC-NUMBER" and len(iteri[1]) != 0:
                pageInArray.insert(i,"* '''EC Number (Pathway Tools)'''{{#set:evidence=EC-NUMBER}}\n")
                i += 1
                for Gname in iteri[1]:
                    pageInArray.insert(i,"** [["+Gname+"]] {{#set:gene association="+Gname+" (EC-NUMBER)}}\n")
                    i += 1
            elif iteri[0] == "FUNCTIONAL" and len(iteri[1]) != 0:
                pageInArray.insert(i,"* '''Functional Gap Filling'''{{#set:evidence=GAP-FILLING (Functional)}}: reaction added by functional gap filling")
                i += 1
            elif iteri[0] == "GO-TERM" and len(iteri[1]) != 0:
                pageInArray.insert(i,"* '''Gene Ontology Term (Pathway Tools)'''{{#set:evidence=GO-TERM}}\n")
                i += 1
                for Gname in iteri[1]:
                    pageInArray.insert(i,"** [["+Gname+"]] {{#set:gene association="+Gname+" (GO-TERM)}}\n")
                    i += 1
            elif iteri[0] == "ORTHO_AT_SILICO" or iteri[0] == "ORTHO_AT_EXP":
                if len(iteri[1]) != 0:
                    pageInArray.insert(i,"* Orthologs with ''A.thaliana''\n")
                    i += 1
                    for Gname in iteri[1]:
                        pageInArray.insert(i,"** [["+Gname+"]] {{#set:gene association="+Gname+" (ORTHOLOGY)}}\n")
                        i += 1
            elif iteri[0] == "MANUAL" and len(iteri[0]) != 0:
                pageInArray.insert(i,"* Manual Associations''\n")
                i += 1
                for Gname in iteri[1]:
                    pageInArray.insert(i,"** [["+Gname+"]] {{#set:gene association="+Gname+" (MANUAL)}}\n")
                    i += 1
            elif iteri[0] not in allAsso.keys():
                print(iteri[0])
                print(iteri[1])
                raise KeyError("Unknown Association")
    except (StopIteration, TypeError):
        # no assignment
        pass
    """            
    # metacyc enzyme associated
    i = pageInArray.index("== MetaCyc Enzymes associated with this reaction ==\n")+1
    enzymes = (tgdbRef.getDicOfNode()[rlt.getIdIn()] for rlt in tgdbRef.getRelation(nodeId,"out") if rlt.getType() == "catalyses")
    try:
        for e in enzymes:
            pageInArray.insert(i,"* "+e.getMisc()["common_name"][0]+", [http://metacyc.org/META/NEW-IMAGE?object="+e.getMisc()["metacyc_id"][0]+" "+e.getMisc()["metacyc_id"][0]+"\n")
            i += 1
    except StopIteration:
        pass
    """
    #HMM hits
    if HMM is not None:
        i = pageInArray.index("== Non validated associations (HMM hits) ==\n")+1
        for h in HMM:
            enzymeMetacycID = tgdbp.getDicOfNode()[h.getIdIn()].getMisc()["metacyc_id"][0]
            pageInArray.insert(i,"* "+enzymeMetacycID+", "+h.getMisc()["HMM"]+" (["+enzymeMetacycID+"]))")
            i += 1
    #External links
    i = pageInArray.index("== External links ==\n")+1
    xref = (tgdbp.getDicOfNode()[rlt.getIdOut()] for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "has xref")
    try:
        for x in xref:
            toInsert = xrefLink(x)
            if toInsert is not None:
                pageInArray.insert(i,toInsert)
                i += 1
    except StopIteration:
        #no xref                    
        pass
    return(pageInArray)

def mp_createWikiPagePathway(tuplId):
    """
    multiProcessing version of the function.
    input: tuplId: <tuple>  tuplId[0]: <int> unique_id access
                            tuplId[1]: <string> metacyc_id access
    output: pageInArray <List>: corresponding to the wikiPage
    """
    pageInArray = createWikiPagePathway(tgdbRef,newTgdbp,tuplId[0],"id")
    fileName = para.path_Resultats+"pathways/"+tuplId[1]+".txt"
    createWikiFile(pageInArray,fileName)
    
def createWikiPagePathway(tgdbRef,tgdbp,_arg,_type):
    """
    create a file with all the wikicode to create the page of the given Pathway
    input:  tgdbRef: <TGDB>: tgdb of metacyc
            tgdbp: <TGDBP> : tgdbplus of the current network
            _arg: <string>: node acces (unique_id,metacyc_id,common_name)
            _type: <string>: refere to the node acess (id,metacyc,cname)
            
    output: list pageinArray
    """
    try:
        nodeId,node = tgdbp.getNodeId(_arg,_type)
        _class = node.getClass()
        if _class != "pathway":
            raise TypeError
    except TypeError:
        print("Unable to find the node with given arguments")
        return False
        
    PmetacycID = node.getMisc()["metacyc_id"][0]
    with open(para.pathway_template) as f:
        pageInArray = f.readlines()
        #2nd line is where the reaction name is defined
        #if from metacyc, then use hyperlink to metacyc.org
    if "Manual" not in PmetacycID:
        pageInArray[1] = pageInArray[1].replace("pathway_metacycID",PmetacycID)
    #in case of reaction added manually, do not use the metacyc link
    else:
        pageInArray[1] = "== Pathway "+PmetacycID+" == {{#set:metacyc id="+PmetacycID+"}}\n"
    #check if common name associated
    if "common_name" in node.getMisc().keys():
        i = pageInArray.index("* Common name:\n")+1
        for cname in node.getMisc()["common_name"]:
            pageInArray.insert(i,"** "+cname+"{{#set:name="+cname+"}}\n")
            i += 1
    #check synonymous ('has name' relations) / generator of 'has name' relations
    names = [rlt for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "has name"]
    if len(names) != 0:
        i = pageInArray.index("* Synonyms:\n")+1
        for synRLT in names:
            syn = tgdbp.getDicOfNode()[synRLT.getIdOut()].getMisc()["label"][0]
            pageInArray.insert(i,"** "+syn+"{{#set:name="+syn+"}}\n")
            i += 1
    #check nb reactions found in metacyc and in current network(if pathway not created...)
    i = pageInArray.index("== Reactions found == {{#set:number of reactions found=0}}\n")
    reactionsFound = [tgdbp.getDicOfNode()[rlt.getIdIn()].getMisc()["metacyc_id"][0] for rlt in tgdbp.getRelation(nodeId,"out") if rlt.getType() == "is in pathway"]
    pageInArray[i] = pageInArray[i].replace("0",str(len(reactionsFound)))
    i += 1
    for r in reactionsFound:
        pageInArray.insert(i,"* [http://metacyc.org/META/NEW-IMAGE?object="+r+" "+r+"]\n")
        i += 1

    if "Manual" not in PmetacycID:
        reactionsTotal = [tgdbRef.getDicOfNode()[rlt.getIdIn()].getMisc()["metacyc_id"][0] for rlt in tgdbRef.getRelation(nodeId,"out") if rlt.getType() == "is in pathway"]
        reactionsNotFound = set(reactionsTotal).difference(set(reactionsFound))

        i = pageInArray.index("== Reaction NOT found == {{#set:number of reactions NOT found=0}}\n")
        if len(reactionsNotFound) != 0:
            pageInArray[i] = pageInArray[i].replace("0",str(len(reactionsNotFound)))
            i += 1
            for r in reactionsNotFound:
                pageInArray.insert(i,"* [http://metacyc.org/META/NEW-IMAGE?object="+r+" "+r+"]\n")
                i += 1
    #External links
    i = pageInArray.index("== External links ==\n")+1
    xref = (tgdbp.getDicOfNode()[rlt.getIdOut()] for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "has xref")
    try:
        for x in xref:
            toInsert = xrefLink(x)
            if toInsert is not None:
                pageInArray.insert(i,toInsert)
                i += 1
    except StopIteration:
        #no xref                    
        pass
    return(pageInArray)

def mp_createWikiPageMetabolite(tuplId):
    """
    multiProcessing version of the function.
    input: tuplId: <tuple>  tuplId[0]: <int> unique_id access
                            tuplId[1]: <string> metacyc_id access
    output: pageInArray <List>: corresponding to the wikiPage
    """
    pageInArray = createWikiPageMetabolite(tgdbRef,newTgdbp,tuplId[0],"id")
    fileName = para.path_Resultats+"metabolites/"+tuplId[1]+".txt"
    createWikiFile(pageInArray,fileName)
    return(tuplId[0])

def createWikiPageMetabolite(tgdbRef,tgdbp,_arg,_type):
    """
    create a file with all the wikicode to create the page of the given Metabolite
    input:  tgdbRef: <TGDB>: tgdb of metacyc
            tgdbp: <TGDBP> : tgdbplus of the current network
            _arg: <string>: node acces (unique_id,metacyc_id,common_name)
            _type: <string>: refere to the node acess (id,metacyc,cname)
            
    output: list pageinArray
    """
    try:
        nodeId,node = tgdbp.getNodeId(_arg,_type)
        _class = node.getClass()
    except TypeError:
        print("Unable to find the node with given arguments")
        return False

    MmetacycID = node.getMisc()["metacyc_id"][0]
    with open(para.metabolite_template) as f:
        pageInArray = f.readlines()
        #2nd line is where the reaction name is defined
        #if from metacyc, then use hyperlink to metacyc.org
    if "Manual" not in MmetacycID:
        pageInArray[1] = pageInArray[1].replace("metabolite_metacycID",MmetacycID)
    #in case of reaction added manually, do not use the metacyc link
    else:
        pageInArray[1] = "== Metabolite "+MmetacycID+" == {{#set:metacyc id="+MmetacycID+"}}\n"
    #check if common name associated
    if "common_name" in node.getMisc().keys():
        i = pageInArray.index("* Common name:\n")+1
        for cname in node.getMisc()["common_name"]:
            pageInArray.insert(i,"** "+cname+"{{#set:name="+cname+"}}\n")
            i += 1
    #check synonymous ('has name' relations) / generator of 'has name' relations
    names = [rlt for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "has name"]
    if len(names) != 0:
        i = pageInArray.index("* Synonyms:\n")+1
        for synRLT in names:
            syn = tgdbp.getDicOfNode()[synRLT.getIdOut()].getMisc()["label"][0]
            pageInArray.insert(i,"** "+syn+"{{#set:name="+syn+"}}\n")
            i += 1        
    #reactions that consume or produce the compound
    produce = (tgdbp.getDicOfNode()[rlt.getIdIn()] for rlt in tgdbp.getRelation(nodeId,"out") if rlt.getType() == "has right")
    consume = (tgdbp.getDicOfNode()[rlt.getIdIn()] for rlt in tgdbp.getRelation(nodeId,"out") if rlt.getType() == "has left")
    unknown = []
    i = pageInArray.index("== Reactions known to consume the compound: ==\n")+1
    try:
        for n in consume:
            try:
                RmetacycID = n.getMisc()["metacyc_id"][0]
                if n.getMisc()["direction"][0] != "REVERSIBLE":
                    pageInArray.insert(i,"* [["+RmetacycID+"]]{{#set:consumed by="+RmetacycID+"}}\n")
                    i += 1
                else:
                    unknown.append(RmetacycID)
            except KeyError:
                pass
    #0 reactions that consume
    except StopIteration:
        pass
    i = pageInArray.index("== Reactions known to produce the compound: ==\n")+1
    try:
        for n in produce:
            RmetacycID = n.getMisc()["metacyc_id"][0]
            try:
                if n.getMisc()["direction"][0] != "REVERSIBLE":
                    pageInArray.insert(i,"* [["+RmetacycID+"]]{{#set:produced by="+RmetacycID+"}}\n")
                    i += 1
                else:
                    unknown.append(RmetacycID)
            except KeyError:
                pass
    #0 reactions that produce
    except StopIteration:
        pass
    i = pageInArray.index("== Reactions of unknown directionality: ==\n")+1
    for R in unknown:
        pageInArray.insert(i,"* [["+R+"]]{{#set:produced or consumed by="+R+"}}\n")
        i += 1
    #External links
    i = pageInArray.index("== External links ==\n")+1
    xref = (tgdbp.getDicOfNode()[rlt.getIdOut()] for rlt in tgdbp.getRelation(nodeId,"in") if rlt.getType() == "has xref")
    try:
        for x in xref:
            toInsert = xrefLink(x)
            if toInsert is not None:
                pageInArray.insert(i,toInsert)
                i += 1
    except StopIteration:
        #no xref                    
        pass
    return(pageInArray)


def xrefLink(xrefNode):
    if xrefNode.getMisc()["db"][0] == "METACYC":
        toInsert = "* pubchem : [http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "uniprot":
        toInsert = "* uniprot : [http://www.uniprot.org/uniprot/"+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"]) {{#set:uniprot id="+xrefNode.getMisc()["id"][0]+"}}\n"

    elif xrefNode.getMisc()["db"][0] == "kegg":
        toInsert = "* kegg : [http://www.genome.jp/dbget-bin/www_bget?"+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"]) {{#set:kegg id="+xrefNode.getMisc()["id"][0]+"}}\n"

    elif xrefNode.getMisc()["db"][0] == "RHEA":
        toInsert = "* RHEA : [http://www.ebi.ac.uk/rhea/reaction.xhtml?id="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "wikipedia":
        toInsert = "* wikipedia : [http://en.wikipedia.org/wiki/"+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "chebi":
        toInsert = "* chebi : [http://www.ebi.ac.uk/chebi/searchId.do?chebiId="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"]) {{#set:chebi id="+xrefNode.getMisc()["id"][0]+"}}\n"

    elif xrefNode.getMisc()["db"][0] == "pubchem":
        toInsert = "* pubchem : [http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "ecocyc":
        toInsert = "* ecocyc : [http://metacyc.org/ECOLI/NEW-IMAGE?object="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "CHEMSPIDER":
        toInsert = "* CHEMSPIDER : [http://www.chemspider.com/Chemical-Structure."+xrefNode.getMisc()["id"][0]+".html "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "umbbd-compounds":
        toInsert = "* umbbd-compounds : [http://umbbd.ethz.ch/servlets/pageservlet?ptype=c&compID="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "ARACYC":
        toInsert = "* ARACYC : [http://metacyc.org/ARA/NEW-IMAGE?object="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "PIR":
        toInsert = "* PIR : [http://pir.georgetown.edu/cgi-bin/nbrfget?uid="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "NCI":
        toInsert = "* NCI : [http://cactus.nci.nih.gov/ncidb2.2/?nsc="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "knapsacK":
        toInsert = "* knapsacK : [http://kanaya.naist.jp/knapsack_jsp/information.jsp?word="+xrefNode.getMisc()["id"][0]+" "+xrefNode.getMisc()["id"][0]+"])\n"

    elif xrefNode.getMisc()["db"][0] == "manual":
        toInsert = "* manual: Added manually "        
    
    else:
        toInsert = "* "+xrefNode.getMisc()["db"][0]+" : "+xrefNode.getMisc()["id"][0]+"\n"
                
    return(toInsert)                

    
def createWikiFile(pageInArray,fileName):
    with open(fileName,'w') as f:
        for line in pageInArray:
            f.write(line)

def wikiUpdate(dirWikiPages,allMetacycId2Delete = None):
    """
    Send and Delete WikiPages of a given wiki (in parameters.py)
    input:  dirWikiPages: <string> Path of the folder where are the folder 'genes' 'pathways' 'reactions' and 'metabolites'
            allMetacycId2Delete: <list> list of metacyc_id corresponding to the pages names to delete
    """
    if allMetacycId2Delete is not None:
        for metacycID in allMetacycId2Delete:
            deletePage(metacycID)
        print("All pages deleted\n")
    
	p = Pool(processes=cpu_count())
	allPages = []
	for folders in ["genes","reactions","pathways","metabolites"]:
		for wikiPage in os.listdir(para.path_Resultats+folders):
			wikiPage = para.path_Resultats+folders+"/"+wikiPage
			allPages.append(wikiPage)

	cSize = int(len(allPages)/cpu_count())+1
	resultats = p.imap(sendPage, allPages, chunksize = cSize)
	[None for _ in resultats]    

def sendPage(wikiPage):
    pageName = wikiPage.replace(".txt","")
    if "/" in pageName:
        pageName = pageName.split("/")[-1]
    print("PN: "+pageName)
    print("WP: "+WikiPage)
    #os.system("php ./lib/wikiManager/sendPage.php "+pageName+" "+wikiPage)
    
def deletePage(pageName):
    os.system("php ./lib/wikiManager/deletePage.php "+pageName)
