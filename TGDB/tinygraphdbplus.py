# -*- coding: utf-8 -*-
# coding: utf8
"""
Created on Thu Apr 23 10:58:12 2015
Version: 1.0.3 - 25-01-16
@author: Meziane AITE, meziane.aite@inria.fr
Tinygraphdbplus is an object representing a DB of metabolic network.
contain <Policy>, <Node> and <Relation>
The policy define the way Node and Relation are associated
A node is an Object that contains information about an element of the network 
(can be a pathway, reaction...).
A realtion defines how two nodes are connected. In a relation there is 
a node "in" and a node "out". (reactionX'in' has left metaboliteX'out')
Tinygraphdbplus is defined by 
    a dictionary of node: key=Node's unique id / value = <Node>
    a tuple of <Relation>
    and a <policy>

#TODO revoir TOUTES LES FONCTIONS UNE PAR UNE
#TODO faire la doc !!
#TODO check Pep8, pour toute la lib/...
#TODO probleme defintion exact d'un metabolite car bcp de class diff;.
"""


#from __future__ import unicode_literals
#from multiprocessing import Pool, cpu_count
from policy import Policy
from node import Node
from relation import Relation
from tinygraphdb import Tinygraphdb
import re, os, collections, sbmlPlugin
import parameters as para
"""try:
    from pyexcel_ods3 import ODSWriter
except:
    print("package pyexcel-ods needed, use this cmd:\n pip install "
          + "pyexcel-ods3")
    exit()"""
try:
    from libsbml import *
except:
    print("package libsbml needed, use this cmd:\n pip install "
          + "python-libsbml")
    exit()
    
class Tinygraphdbplus:
    def __init__(self,tgdbpFilePath = None):
        if tgdbpFilePath is not None:
            with open(tgdbpFilePath) as f:
                tgdbpInArray = f.readlines()
            self.copyPolicy(tgdbpInArray)
            self.copyGraph(tgdbpInArray)
        else:
            self.tuplOfRelation = ()
            self.dicOfNode = {}
            self.policy = Policy()
            self.policy.setPolicyInArray(para.policyInArray)
            
#==============================================================================
# Constructor / getter            
#==============================================================================

    def copyPolicy(self,source):
        """
        allow to copy the policy of a tgdbp stored in a list (ex after reading
        a .tgdbp with an readlines())
        input: tgdbpInArray <list>
        OR copy the policy from a <Tinygraphdb> object
        input: tgdb <Tinygraphdb>
        """
        if type(source) is list:
            self.policy = Policy(source)
        else:
            self.policy = _from.getPolicy()


    def getPolicy(self):
        return self.policy


    def initTgdbplus(self, tgdbRef, key, tgdbpName, assocGeneReaction,
                     assocReactionHMM = None, sbml = None):
        """
        Allow to initialise a tgdbp from a list of association reaction-gene, 
        a list of association reaction-HMM and a tgdb of reference 
        Input:
        tgdbRef: <tgdb> tgdb of reference, a database of reaction
                (ex metacyc_18.0.tgdb).
        key: <string> This is the key used to recovere the reaction from the
                tgdbRef (ex: "id", "common_name", "metacyc_id" ...)
        tgdbpName : <string> The name of the new tgdbp (ex: Tiso_1.0.tgdbp).
        assoGeneReaction : <string> File's name where are listed the reaction 
                            and the genes associated with. sep = " ".
        (optional) assoReactionHMM : <string> File's name where are listed the 
                        reaction with protein associated with an HMM score.         
        sbml : <bool> if True, also generate an sbml file.
        Output:
        tgdbplus file and an sblm file (if sbml = True)
        """
        # assocGeneReaction, recover all the reactions names in listOfReaction and
        # the lengths. And create a dictionary: key = genes's name / value:
        # list of tuple(reaction_id,Type of assignment)
        assocGeneReaction = {}
        #open the file
        with open(assocGeneReaction,'r') as f:
            for line in f:
                line = line.replace("\n","")
                if len(line) != 0:
                    line = line.split(" ")
                    #line[0] = reaction_id
                    #line[1] = gene_id
                    #line[2] = type of association
                    try:
                        assocGeneReaction[line[0]].append((line[1],line[2]))
                    except KeyError:
                        assocGeneReaction[line[0]] = [(line[1],line[2])]
        nbReaction = len(assocGeneReaction.keys())
        nbGene = len([i for i in assocGeneReaction.values()[0]])
        total = nbReaction + nbGene

        # Optional:
        # Creation of a dictionary: key = protein name associated to
        # reactions/ value: list of tuple (reaction_id,HMM)
        # Data are recovered from assocReactionHMM
        dicOfHMM = {}
        if assocReactionHMM is not None:
            with open(assocReactionHMM,'r') as f: #open the file               
                for line in f:    
                    line = line.replace("\n","")
                    if len(line) != 0:
                        line = line.split("\t")
                        #line[0] = reaction_id
                        #line[1] = protein_id
                        #line[2] = HMM score
                        try:
                            dicOfHMM[line[1]].append((line[0],line[2]))
                        except KeyError:
                            dicOfHMM[line[1]] = [(line[0],line[2])]

        #copy all the reactions from the tgdbRef and create the genes's nodes
        count = 1
        for k,v in assocGeneReaction.iteritems():
            #TODO Finir cette boucle, reaction unique id ;..
            #k: reaction_id, v: (gene_id,assoc)
            print count,"/",total
            try:
                self.copyNode(tgdbRef, k, key)
                for assoc in v:
                    #assoc[0] = gene_id
                    #assoc[1] = type of assoc
                    if self.getNode(assoc[0],"origin_id",True) is None:
                        #gene node doesnt exist, creating it
                        self.createNode("gene",{"origin_id":[assoc[0]]},["self","is associated with",])
            except TypeError:
                print "Unable to get the node with arg:",R,"and type:",key
            count += 1
        
        # create and add the protein node and relation            
        _max = len(dicOfHMM.keys())
        if _max != 0:
            _now = 1
            for k in dicOfHMM.iterkeys():
                print(str(_now)+"/"+str(_max))
                self.createProtein([k],["manual",0],dicOfHMM[k])
                _now += 1
                
        self.generateFile(para.path_SpecificFiles+newTgdbName)


    def copySbml(self,sbmlFile, tgdbRef, assocIdOriginRef = None,verbose = False):
        """
        Allow to initialise a tgdbp from an sbml. If the id of the sbml are 
        different with the tgdbRef, need to add a dictionnary of associations
        between the id in the sbml and the id of the database of reference.
        Input:        
        sbmlFile: <string> name of the sbml file
        tgdbRef: <tgdb> tgdb of reference.
        assocIdOriginRef (opt): <string> name of the file containing the 
                                association original_id ref_id, sep ="\t"
        verbose: <bool> if True print supp info
        #TODO plus generique metacyc_id/biocyc
        """
        #using libSbml to read sbmlFile
        if verbose:
            print ("loading sbml file: " + sbmlFile)
        reader = SBMLReader()
        document = reader.readSBML(sbmlFile)
        model = document.getModel()
        listOfSpecies = model.getListOfSpecies()
        listOfReactions = model.getListOfReactions()
        nbReactions = len(listOfReactions)
        nbSpecies = len(listOfSpecies)
        if verbose:
            print("nb species: " + str(nbSpecies))
            print("nb reactions: " + str(nbReactions)) 
            
        dicOfAssocReactions = {}
        dicOfAssocSpecies = {}
        #reading assocIdOriginRef line by line, one line = "origin_id\tref_id\n"
        if assocIdOriginRef is not None:
            with open(assocIdOriginRef,'r') as f: #open the file               
                for line in f:
                    line = line.replace("\n","")
                    line = line.split("\t")
                    (idOrigin,idRef) = (line[0],line[1]) 
                    #recovere the node class
                    nodeClass = tgdbRef.getDicOfNode()[idRef].getClass()
                    #in case of reaction
                    if nodeClass == "reaction":
                        dicOfAssocReactions.update({idOrigin:idRef})
                    #in case of species
                    else:
                        dicOfAssocSpecies.update({idOrigin:idRef})
        #association is recovered in the smbl, part 'notes' of elements
        else:
            for species in listOfSpecies:
                #parsing the notes section in a dictionnary
                dicOfNotes = sbmlPlugin.parseNotes(species)
                try:
                    #TODO: now is specific for metacyc, need to use var instead of 'biocyc'
                    #check if there is biocyc crossid
                    dicOfAssocSpecies[species.getId()] = dicOfNotes["BIOCYC"][0]
                except KeyError:
                    #no crossid in the tgdbref
                    dicOfAssocSpecies[species.getId()] = "NA"
            for reaction in listOfReactions:
                dicOfNotes = sbmlPlugin.parseNotes(reaction)
                try:
                    dicOfAssocReactions[reaction.getId()] = dicOfNotes["BIOCYC"][0]
                except KeyError:
                    dicOfAssocReactions[reaction.getId()] = "NA"

        
        if verbose:
            print("start with reaction")
        #dictionnary used to stock association gene:reaction
        dicOfGeneReaction = {}
        count = 0
        for (idOrigin,idRef) in dicOfAssocReactions.iteritems():
            count += 1
            #recovere the reaction element from sbml
            reactionSBML = listOfReactions.getElementBySId(idOrigin)
            nextStep = False
            if verbose:
                print(str(count)+"/"+str(nbReactions))
                print("idOrigin: "+str(idOrigin)+"\t idRef: "+str(idRef))
            try:
                #check if reaction already in the tgdbp
                nodeId,node = self.getNode(idRef,"metacyc_id",True)[0]
                nextStep = True
            except TypeError:
                try:
                    #copy the node reaction and dependency relations/nodes cf copyNode()
                    if verbose:
                        print("Try to copy node from tgdbref")
                    self.copyNode(tgdbRef,idRef,"metacyc_id")
                    nodeId,node = self.getNode(idRef,"metacyc_id",True)[0]
                    nextStep = True
                except TypeError:
                    print("Not in metacyc")
            if nextStep:
                #Extracting all data to create the supplementary data node
                if verbose:
                    print("Creating suppData")
                formula = sbmlPlugin.extractFormula(reactionSBML)
                notes = sbmlPlugin.parseNotes(reactionSBML)
                data = {"origin_file":[sbmlFile],"origin_id":[str(idOrigin)],
                "name":[reactionSBML.getName()],"reversible":[str(reactionSBML.getReversible())],
                "formula":[formula]}
                data.update(notes)
                self.createNode("suppData",data,[[nodeId,"has suppData","_self"]])
                #parses gene_association and create gene node or update already existing genes
                if "GENE_ASSOCIATION" in notes.keys():
                    listOfGenes = sbmlPlugin.parseGeneAssoc(notes["GENE_ASSOCIATION"][0])
                    for gene in listOfGenes:
                        if gene in dicOfGeneReaction.keys():
                            dicOfGeneReaction[gene].append(nodeId)
                        else:
                            dicOfGeneReaction[gene] = [nodeId]

        if verbose:
                print("Creates gene's nodes:")
        count = 0
        nbGenes = len(dicOfGeneReaction.keys())
        for (k,v) in dicOfGeneReaction.iteritems():
            count += 1
            if verbose:
                print(str(count)+"/"+str(nbGenes))
            
            try:
                #check if gene already in the tgdbp
                nodeId,node = self.getNode(k,"origin_id",True)[0]
            except TypeError:
                data = {"origin_id":[k]}
                nodeId,node = self.createNode("gene",data)
            for i in v:
                rlt = Relation([i,"is linked to",nodeId])
                self._addRelation(rlt)
                        
        if verbose:
                print("Case species:")
        count = 0
        #in case of species
        for (idOrigin,idRef) in dicOfAssocSpecies.iteritems():
            count += 1
            speciesSBML = listOfSpecies.getElementBySId(idOrigin)
            nextStep = False
            if verbose:
                print(str(count)+"/"+str(nbSpecies))
                print("idOrigin: "+str(idOrigin)+"\t idRef: "+str(idRef))
            try:
                #check if species is already in the tgdbp
                nodeId,node = self.getNode(idRef,"metacyc_id",True)[0]
                nextStep = True
            except TypeError:
                try:
                    #copy the node species cf _copyNodeExtend()
                    if verbose:
                        print("Try to copy node from tgdbRef")
                    nodeId,node = tgdbRef.getNode(idRef,"metacyc_id",True)[0]
                    self._copyNodeExtend(tgdbRef,nodeId)
                    nextStep = True
                except TypeError:
                    print("Not in tgdbRef")
            if nextStep:
                #Extracting all data to create the supplementary data node
                if verbose:
                    print("Creating suppData")
                notes = sbmlPlugin.parseNotes(speciesSBML)
                try:
                    notes.pop("INCHI")
                except KeyError:
                    pass
                data = {"origin_file":[sbmlFile],"origin_id":[str(idOrigin)],
                "name":[speciesSBML.getName()],"charge":[str(speciesSBML.getCharge())],
                "compartment":[speciesSBML.getCompartment()]}
                data.update(notes)
                self.createNode("suppData",data,[[nodeId,"has suppData","_self"]])

    def copyGraph(self,tgdbpInArray):
        """
        Allow to recover all the informations of the tgdbp file stored in a list.
        stock all the nodes in a dictionnary "self.dicOfNode", key = node id / value = node object
        stock all the relations in a tuple "self.tuplOfRelation"
        Input: tgdbpInArray <list>
        """
        self.dicOfNode = {}
        self.dbNotes = {}
        listOfRelation = []
        try:
            dbIndex = tgdbpInArray.index("Data Base informations\n")
        except ValueError:
            pass
        #Index where start Nodes
        nodeIndex = tgdbpInArray.index("Nodes\n")
        #Index where start Relations       
        relationIndex = tgdbpInArray.index("Relations\n")
        
        #
        try:
            dbSection = [line.replace("\n","") 
            for line in tgdbpInArray[dbIndex+1:nodeIndex] if line != "\n"]
            #
            for line in dbSection:
                if "\t" not in line:
                    line = line.replace(":","")
                    dbNotes[line] = {}
                    currentDb = line
                else:
                    line = line.replace("\t","").split(":")
                    dbNotes[currentDb][line[0]] = line[1]
        except NameError:
            pass
        # generator of data to input in Node()
        nodeSection = [line.replace("\n","").split("\t") 
        for line in tgdbpInArray[nodeIndex+1:relationIndex] if line != "\n"]
        #
        for data in nodeSection:
            #Create a new Node object (cf node.py)                
            node = Node(data) 
            #add the node into the dictionnay
            self.dicOfNode[node.getId()] = node 

        # generator of data to input in Relation()
        relationSection = (line.replace("\n","").split("\t") 
        for line in tgdbpInArray[relationIndex+1:len(tgdbpInArray)] if line != "\n")
        #instantiate a new Relation object (cf relation.py)
        for data in relationSection:
            relation = Relation(data)
            #stock in a list all the relations
            listOfRelation.append(relation)
        # then change list into tuple
        self.tuplOfRelation = tuple(listOfRelation)
                
        
    def getDicOfNode(self):
        return self.dicOfNode

    
    def getTuplOfRelation(self):
        return self.tuplOfRelation

    
    def generateFile(self, fileName = "newTGDB.tgdbp"):
        """
        Allow to create a file tgdbp to stock all the data.
        Input: fileName <string> the file name where to stock the output
        Output: file .tgdbp
        """
        # Order the dictionary of node by unique id and the tuple of relation
        # by the node in id.
        dicKeys = self.getDicOfNode().keys()
        dicKeys.sort()
        orderedTuplOfRelation = tuple(sorted(self.tuplOfRelation,
                                           key=lambda x: x.idIn, reverse=False))
        with open(fileName,'w') as f:
            # It writes the policy of the TGDBP file.
            f.write("Policy\n")
            policyInArray = self.policy.getPolicyInArray()
            for line in policyInArray:
                line = "\t".join(line)
                line = line + "\n"
                f.write(line)
            f.write("\n")
            # It writes the nodes of the TGDBP file.
            f.write("Nodes\n")
            f.write("\n")
            for nodeId in dicKeys:
                node = self.getDicOfNode()[nodeId]
                line = node.toString()+"\n"
                f.write(line)
            f.write("\n")
            # It writes the relations of the TGDBP file.
            f.write("Relations\n")
            f.write("\n")
            for rlt in orderedTuplOfRelation:
                line = rlt.toString()+"\n"
                f.write(line)

    def extract_pathway(self, _arg, _type, tgdbRef_file, output, sbml = None): 
        """
        #TODO completement obsolete !
        extractNode allow to recovere a node and all information around this 
        node  in a ods file
        input: node access  
        output: file ods, "metacycidOftheNode.ods" and file 
        metacycidOftheNode.sbml (if sbml is not none)    
        """
        #Retriving the ID and the node of the pathway.
        node_id, node = self.getNode(_arg,_type)[0]
        node_class = node.getClass()
        assert node_class == "pathway"
        
        tgdbRef = Tinygraphdb(tgdbRef_file)
        #Retriving all the reactions associated to the pathway from the tgdbRef
        total_reactions = [tgdbRef.getDicOfNode()[rlt.getIdIn()] for rlt in tgdbRef.getRelation(node_id,"out")
        if rlt.getType() == "is in pathway"
        and tgdbRef.getDicOfNode()[rlt.getIdIn()].getClass() == "reaction"]
        #Retriving the reactions (ID) present in the network
        found_reactions = [self.getDicOfNode()[rlt.getIdIn()].getId() for rlt in self.getRelation(node_id,"out")
        if rlt.getType() == "is in pathway"
        and self.getDicOfNode()[rlt.getIdIn()].getClass() == "reaction"]

        if len(found_reactions) == 0:
            print("0 reactions associated to this pathway in the network")
            return
        
        with open(output,'w') as f:
            #Define header
            header = ("Reactions (metacyc_id)", "Reactions (common_name)", "EC-Number",
                      "Formula (metacyc_id)", "Formula (common_name)", "Found in the network")
            header = "\t".join(header)+"\n"
            f.write(header)
            for rNode in total_reactions:
                rId = rNode.getId()
                metacyc_id = rNode.getMisc()["metacyc_id"][0]
                if rId in found_reactions:
                    in_network = "yes"
                else:
                    in_network = "no"
                try:
                    ec = rNode.getMisc()["ec"][0]
                except KeyError:
                    ec = "Unknown"
                try:
                    common_name = rNode.getMisc()["common_name"][0]
                except KeyError:
                    common_name = "Unknown"
                try:
                    direction = rNode.getMisc()["direction"][0]
                except KeyError:
                    direction = " =>/<=> "
                if direction == "REVERSIBLE":
                    direction = " <=> "
                elif direction == "LEFT-TO-RIGHT":
                    direction = " => "
        
                reactants = [rlt.getMisc()["stoichiometry"][0]+" "+tgdbRef.getDicOfNode()[rlt.getIdOut()].getMisc()["metacyc_id"][0] 
                for rlt in tgdbRef.getRelation(rId,"in") if rlt.getType() == "consumes"]
                products = [rlt.getMisc()["stoichiometry"][0]+" "+tgdbRef.getDicOfNode()[rlt.getIdOut()].getMisc()["metacyc_id"][0]
                for rlt in tgdbRef.getRelation(rId,"in") if rlt.getType() == "produces"]
                metIdFormula = " + ".join(reactants)+direction+" + ".join(products)
                
                try:
                    reactants = [rlt.getMisc()["stoichiometry"][0]+" "+tgdbRef.getDicOfNode()[rlt.getIdOut()].getMisc()["common_name"][0] 
                    for rlt in tgdbRef.getRelation(rId,"in") if rlt.getType() == "consumes"]
                    products = [rlt.getMisc()["stoichiometry"][0]+" "+tgdbRef.getDicOfNode()[rlt.getIdOut()].getMisc()["common_name"][0]
                    for rlt in tgdbRef.getRelation(rId,"in") if rlt.getType() == "produces"]
                    cnameFormula = " + ".join(reactants)+direction+" + ".join(products)
                except KeyError:
                    cnameFormula = "Unknown"
                    
                line = "\t".join([metacyc_id,common_name,ec,metIdFormula,cnameFormula,in_network])
                line = line+"\n"
                f.write(line)
        if sbml is not None:
        #generate an sbml for the extracted data
            print("Generating SBML file...")
            toExtract = Tinygraphdbplus()
            toExtract.copyNode(self, _arg, _type, "")
            toExtractTgdbName = str(node.getMisc()["metacyc_id"][0])
            toExtractTgdbName += ".tgdbp"
            toExtract.generateFile(toExtractTgdbName)
            sbmlName = para.path_Resultats+str(node.getMisc()["metacyc_id"][0])+".sbml"
            os.system("./sbml/tgdb2sbml" + " " + toExtractTgdbName +" "
                      + sbmlName + " " + str(para.species))
            os.system("rm " + toExtractTgdbName)
        return True                

        
    def get_all_pathways(self, tgdbRef_file, output, verbose = False):
        """
        Recover data of all the pathways of the network in tbl file (sep = "\t")
        Input: 
        tgdbRef: <Tinygraphdb> the database of reference
        Output:
        fileName <string> path of the output file.
        #TODO update
        """
        tgdbRef = Tinygraphdb(tgdbRef_file)
        
        pathways = [node for node in self.getDicOfNode().values()
        if node.getClass() == "pathway"]
        _max = len(pathways)

        with open(output,'w') as f:
            header = ["Metacyc_id", "Common_name", "Number of reaction found", 
            "Total number of reaction", "Ratio (Reaction found / Total)"]
            header = "\t".join(header)+"\n"
            f.write(header)

            count = 1
            for node in pathways:
                metacyc_id = node.getMisc()["metacyc_id"][0]
                if verbose:
                    print("Pathway : "+metacyc_id+" "+str(count)+"/"+str(_max))
                # Recover the first common_name
                try:
                    common_name = node.getMisc()["common_name"][0]
                except KeyError:
                    common_name = "Unknown"
                
                number_of_reaction_found = len([rlt for rlt in self.getRelation(node.getId(),"out")
                if rlt.getType() == "is in pathway"
                and self.getDicOfNode()[rlt.getIdIn()].getClass() == "reaction"])

                try:
                    total_number_of_reaction = len([rlt for rlt in tgdbRef.getRelation(node.getId(),"out")
                    if rlt.getType() == "is in pathway"
                    and tgdbRef.getDicOfNode()[rlt.getIdIn()].getClass() == "reaction"])
                    # If keyError: pathway not in tgdbRef, pathway added manualy
                except KeyError: 
                    total_number_of_reaction = "NA"
                    
                try:
                    if type(total_number_of_reaction) is int:
                        ratio = "%.2f" % (float(number_of_reaction_found)/total_number_of_reaction)
                    else:
                        ratio = "NA"
                    line = [metacyc_id,common_name, str(number_of_reaction_found), 
                            str(total_number_of_reaction), str(ratio)]
                    line = "\t".join(line)+"\n"
                    f.write(line)
                except ZeroDivisionError:
                    pass
                count += 1

#==============================================================================
# For Nodes 
#==============================================================================
            
    def getNode(self,_arg,_type,isUnique = True):
        """
        Allow to recover the unique id and the node object by any miscellious
        data.
        If you want to recovere many node that share that misc data,
        set isUniq to False
        input:  _arg <string> : the data used to recovere a node
                _type <string> : the key of that data
                isUniq <bool>: if true, will recovere the first occurence 
                                if false, will recovere all the node associated with this data
        output: list of tuple [(x,y),..]: x: <string> the id of the node, y: <node> the node
                None: if the node doesnt exist
        """
        resultat = []
        if _type == "id":
            try:
                node = self.getDicOfNode()[_arg]
                _id = _arg
                resultat.append((_id,node))
            except KeyError:
                print("Unkown ID")
                return None
        if isUnique:
            for k,n in self.getDicOfNode().iteritems():
                if _type in n.getMisc().keys() and _arg in n.getMisc()[_type]:
                    _id = n.getId()
                    node = self.getDicOfNode()[_id]
                    resultat.append((_id,node))
                    break
        else:
            for k,n in self.getDicOfNode().iteritems():
                if _type in n.getMisc().keys() and _arg in n.getMisc()[_type]:
                    _id = n.getId()
                    node = self.getDicOfNode()[_id]
                    resultat.append((_id,node))

        if len(resultat) != 0:
            return resultat
        else:
            return None

    def _addNode(self,node):
        """
        addNode() allows to add a node in the tgdb, only if it does not exist.
        Check the uniqueID
        input: node <node> : the node to add        
        output: bool    True if the node was succesfully added
                        False if the node already exist
        """
        if node.getId() not in self.getDicOfNode().keys():
            self.dicOfNode[node.getId()] = node
            return True
        else:
            return False

        
    def _copyNodeExtend(self, tgdbRef, nodeId):
        """
        Allows to copy a node with the first children only.
        Recursive function, call itself for the relations where the node is "in"
        NB: particular case: we dont want to recovere the relations "prot catalyses reaction"
        do nothing for the relations where the node is "out"
        """
        node = tgdbRef.getDicOfNode()[nodeId]
        # If true, the node does not exist and is susccesffuly added.
        if self._addNode(node):
            try:
                relationsIn = (rlt for rlt in tgdbRef.getRelation(node.getId(),"in")
                if rlt.getType() != "catalyses") 
                # For each relation, we add it with addRelation(), then
                # call _copyNodeExtend() for the id 'out'.
                for rlt in relationsIn:
                    self._addRelation(rlt)
                    nodeOutId = rlt.getIdOut()
                    nodeOutClass = tgdbRef.getDicOfNode()[nodeOutId].getClass()
                    if (nodeOutClass == "xref" or nodeOutClass == "name" 
                    or nodeOutClass == "suppData"):
                        self._addNode(tgdbRef.getDicOfNode()[nodeOutId])
                    else:
                        self._copyNodeExtend(tgdbRef, nodeOutId)                        
            # TypeError is raise if tgdb.getRealtion() is none, not relation
            # is found.
            except TypeError:
                pass

    def copyNode(self, tgdbRef, _arg, _type):
        """
        #NB: for now, do not take care of gene and genes relations. 
        copyNode() allows to copy a node from an other tgdb or tgdbp. It copies all 
        the relations 'in' and 'out' and it calls the function 
        _copyNodeExtend() to recover the associated node.
        Input: tgdb <Tinygraphdb> or 
               tgdbp <Tinygraphdbplus>: the tgdb from where the node is copied.
               _arg: values in the misc dictionnary of the node
               _type: key associated to the _arg 

        """
        try:
            nodeToCopy = tgdbRef.getNode(_arg, _type)
        except TypeError:
            raise TypeError("Unable to get the node(s) with arg: " +str(_arg)+" and type: "+str(_type))

        for (nodeId,node) in nodeToCopy:
            # True => node succeffuly added in dictionary of node.
            if self._addNode(node):
                # Recover all relations of the node
                try:
                    relationsIn = (rlt for rlt in tgdbRef.getRelation(nodeId,"in"))
                    # Add each relation with _addRelation, then call
                    # _copyNodeExtend() for the id 'out'.
                    for rlt in relationsIn:
                        self._addRelation(rlt)
                        nodeOutId = rlt.getIdOut()
                        nodeOutClass = tgdbRef.getDicOfNode()[nodeOutId].getClass()
                        if (nodeOutClass == "xref" or nodeOutClass == "name" 
                        or nodeOutClass == "suppData"):
                            self._addNode(tgdbRef.getDicOfNode()[nodeOutId])
                        else:
                            self._copyNodeExtend(tgdbRef,nodeOutId)        
                # TypeError is raise if tgdb.getRealtion() is none, no relation
                # found. (NoneType not iterable)
                except TypeError:
                    pass                      
    
                try:
                    # Recover all relations where the node is out.
                    relationsOut = (rlt for rlt in tgdbRef.getRelation(nodeId, "out")
                    if rlt.getType() != "catalyses")
                    # For each relation, we add it with addRelation, then call
                    # _copyNodeExtend() for the id 'in'
                    for rlt in relationsOut:
                        self._addRelation(rlt)
                        nodeInId = rlt.getIdIn()
                        self._copyNodeExtend(tgdbRef, nodeInId)
                # TypeError is raised if tgdb.getRealtion() is none, not relation
                # found.
                except TypeError:
                    pass

            
    def _delNodeExtend(self,relation,toCheck):
        """
        #TODO Update
        _delNodeExtend() allows to delete or no a node by checking the given
        relation.
        if the node to check is 'out':
            if the node has at least one realtion where he is 'out': node not 
            deleted.
            if None: call delNode()
        If the node to check is 'in':
            if the node has at least one relation (where he is 'in')
            of the same type that the current deleted: node not deleted
            if None: call delNode()
        input:  relation <Relation> : the relation just deleted in delNode()
                toCheck <String> : "in" or "out" : the side node to check
        """
        # Check the node 'toCheck'.
        if toCheck == "out":
            nodeIdToCheck = relation.getIdOut()
            try:
                relationsOut = (rlt for rlt in self.getRelation(nodeIdToCheck,
                                                                "out"))
                # Next line is useless but it allows to delete the error
                # 'local variable relationsOut not used'...
                relationsOut.next()
            #TypeError raises => getRelation() returns None ... no relations,
            # the node is deleted.
            except TypeError:
                self.delNode(nodeIdToCheck,"id")
        elif toCheck == "in":
            nodeIdToCheck = relation.getIdIn()
            try:
                relationsIn = (rlt for rlt in self.getRelation(nodeIdToCheck,
                                                               "in")
                if rlt.getType() == relation.getType())
                relationsIn.next()    
            # TypeError raises => getRelation() returns None ... no relations,
            # the node is deleted.
            # StopIteration raises => getRelation() returns relations but
            # none of the same type.
            except (TypeError,StopIteration):
                self.delNode(nodeIdToCheck,"id")        

                
    def delNode(self, _arg, _type = "metacyc"):
        """
        #TODO update
        delNode() allows to delete a node and its relations (if there is 
        relations). Firstly, it deletes the node, then it deletes the 
        relation in&out.
        It also just can delete an association, without deleting the 
        specified reaction.
        Input: 
        _arg: (can be the metacyc_id, or the common_name, or the unique_id).
        _type: refer to _arg, can be "metacyc" for metacyc_id, "cname" for 
               common_name or "id" for unique_id. 
        Output: 
        tuple(list or None,list or None).
        """
        try:
            nodeId, node = self.getNodeId(_arg,_type)
        except TypeError:
            return False
        
        # Delete the node from dicOfNode().
        try:
            self.dicOfNode.pop(nodeId)
        except KeyError:
            print("The id "+ str(nodeId) +" doesnt exist. Unable to delete "
                  + "the node.\n")
            return False
            
        # If exist delete the relations 'in' and 'out'
        try:
            # Recover the relations where the node is "in".
            relationsIn = (rlt for rlt in self.getRelation(nodeId,"in"))
            for rlt in relationsIn:
                self._delRelation(rlt)
                if (rlt.getType() == "products"
                or rlt.getType() == "catalyses"):
                    self.delNode(rlt.getIdOut(),"id")
                else:
                    self._delNodeExtend(rlt,"out")
        except TypeError:
            pass
        try:
            # Recover the relations where the node is "out"
            relationsOut = (rlt for rlt in self.getRelation(nodeId,"out"))
            if (node.getClass() == "pathway" 
            or node.getClass() == "reaction"):
                for rlt in relationsOut:
                    self._delRelation(rlt)
                    self._delNodeExtend(rlt,"in")
            else:
                for rlt in relationsOut:
                    self._delRelation(rlt)
                    self._delRelationdelNode(rlt.getIdIn(),"id")
        except TypeError:
            pass
        return True

    
    def updateNode(self, _arg, _type, data, action):
        """
        updateNode allow to update miscellious data of a Node.
        input:  _arg: <string> The value used to acces to the node (ex: the id)
                _type: <string> Define the _arg, can be "metacyc" for 
                metacyc_id, "comme_name" for common_name or "id" for unique_id
                for _arg and _type cf getNode()
                data: <tuple>, data[0] refere to the miscellious data key 
                       (ex: metacyc_id, common_name, direction ...)
                       _data[1] is a list of value to add / update,
                       data[1] can be null if the action is to pop the misc data
                action: <string> : if == "add": the _data[1] wil be added 
                                    (ex: adding a common_name)
                                    if == "remove": the _data[1] will be 
                                    removed (ex: remove just one specifique 
                                    common_name)
                                    if == "pop": the _data[0] will be removed 
                                    (ex: removing all common_name)
                                    if == "update": the _data[1] will replace 
                                    the first value (work only if just one 
                                    value associated, ex direction, 
                                    metacyc_id...)
        ex: updateNode(1234,"id",('direction','LEFT-TO-RIGHT'),update) : the 
            reaction' direction will be change to left2right
        """
        try:
            listOfNode = self.getNodeId(_arg,_type)
        except TypeError:
            print "Unable to get the node with arg:",_arg,"and type:",_type
            return False

        for nodeId,node in listOfNode:
            if action == "add":
                if data[0] in node.getMisc().keys():
                    oldData = node.getMisc()[data[0]]
                    oldData = oldData + data[1]
                    oldData = set(oldData)
                    newData = list(oldData)
                    node.getMisc()[data[0]] = newData
                else:
                    node.getMisc()[data[0]] = data[1]
        
            elif action == "remove":
                if data[0] in node.getMisc().keys():
                    try:
                        oldData = node.getMisc()[data[0]]
                        for i in data[1]:
                            oldData.remove(i)
                        if len(oldData) != 0:
                            node.getMisc()[data[0]] = oldData
                        else:
                            node.getMisc().pop(data[0])
                    except ValueError:
                        print("The value "+str(i)+" in "+str(data[0])
                              +" doesn't exist\n")
                        return False
                else:
                    print("No data "+str(data[0])+" associated to this node\n")
                    return False

            elif action == "pop":
                if data[0] in node.getMisc().keys():
                    node.getMisc().pop(data[0])
                else:
                    print("No data "+str(data[0])+" associated to this node\n")
                    return False
            
            elif action == "update":
                try:
                    if (len(node.getMisc()[_data[0]]) == 1):
                        node.getMisc()[data[0]] = [data[1]]
                    else:
                        print("can not update data with more than one value, "
                              + "choose 'add' or 'remove'\n")
                except KeyError:
                    print("No data "+str(data[0])+" associated to this node\n"
                          + "Creating data...\n")
                    node.getMisc()[data[0]] = [data[1]]
                
            else:
                print("Unknown action: "+str(action)+", please check doc")
                return False
            self.getDicOfNode()[nodeId] = node
            
#==============================================================================
# For Relations:     
#==============================================================================

    def _delRelation(self,relation):
        try:
            for rlt in self.getTuplOfRelation():
                if rlt.compare(relation):
                    _index = self.getTuplOfRelation().index(rlt)
                    break
            listOfRelation = list(self.tuplOfRelation)
            listOfRelation.pop(_index)
            self.tuplOfRelation = tuple(listOfRelation)
        except ValueError:
            print("Unable to delete this relation, doesn't exist.")

            
    def _addRelation(self,relation):
        """
        AddRelation() allows to add a relation if it doesnt exist. Check the 
        type AND the idOut
        Input: <relation> 
        Output: return true if relation was added
                return false if relation already exist
        """
        for rlt in self.getTuplOfRelation():
            if rlt.compare(relation):
                return False
        # The relation doesnt exist
        tmpListOfRelation = list(self.tuplOfRelation)
        # Add the relation to the list
        tmpListOfRelation.append(relation)
        self.tuplOfRelation=tuple(tmpListOfRelation)
        return True

    def getUniqRelation(self,idIn,_type,idOut):
        """
        #TODO DELETE ???
        """
        for i in range(len(self.getTuplOfRelation())):
            rlt = self.getTuplOfRelation()[i]
            if rlt.getIdIn() == idIn and rlt.getIdOut() == idOut:
                return (i,rlt)
                
    def getRelation(self, _id, _dir):
        """
        getRelation() allows to recover from a node id, all the relations
        where this id is 'In' or 'Out'
        input: _id <string> the unique id
                _dir <string> the position of the node in the relation "in" or "out"
        output: tuple of object 'Relation' cf relation.py 
                None: there is no relation associated to the id given 
        """   
        tmpListRelation = []
        for rlt in self.getTuplOfRelation():
            if rlt.getIdIn() == _id and _dir == "in":
                tmpListRelation.append(rlt)
            elif rlt.getIdOut() == _id and _dir == "out":
                tmpListRelation.append(rlt)
        if len(tmpListRelation) == 0:
            return None
        else:
            resultat = tuple(tmpListRelation)
            return resultat    


    def addAssociation(self, gene, comment, _arg, _type="metacyc"):
        """
        It adds only one association: a gene to a reaction.
        Input:  gene: The common name of the gene.
                comment: This string has to one of the following words: 
                         "AUTOMATED-NAME-MATCH", "EC-NUMBER", "FUNCTIONAL",
                         "GO-TERM", "ORTHO_AT_SILICO", "ORTHO_AT_EXP", or 
                         "MANUAL".
                _arg: (can be the metacyc_id, or the common_name, or the 
                      unique_id).
                _type: refer to _arg, can be "metacyc" for metacyc_id, "cname" 
                       for common_name or "id" for unique_id.
        """
        try:
            reacId = self.getNodeId(_arg, _type)[0]
        except TypeError:
            return False
        # In this case, the specified gene already exists, so we just add the
        # association.
        mGene = "Manual-" + gene
        if self.getNodeId(mGene, "metacyc") is not None:
            gNodeId, gNode = self.getNodeId(mGene, "metacyc")
            self.dicOfAssoc[str(gNodeId)].append((reacId, comment))
            relation = Relation([str(gNodeId), "is associated with",
                                 str(reacId), "assignment", comment])
            self._addRelation(relation)                
        # In this case, the specified gene is not exist yet, so we create
        # a page for this gene.
        else:
            self.createGene([gene],["manual",0], [(_arg, comment)])
            gNodeId = self.getNodeId(mGene, "metacyc")[0]
            self.dicOfAssoc[str(gNodeId)] = []
            self.dicOfAssoc[str(gNodeId)].append((reacId, comment))


    def delAssociation(self, gene, _arg, _type = "metacyc"):
        """
        It deletes an association: a gene to a reaction. This association
        has to exist.
        Input:  gene: The common name of the gene.
                _arg: (can be the metacyc_id, or the common_name, or the 
                      unique_id).
                _type: refer to _arg, can be "metacyc" for metacyc_id, "cname" 
                       for common_name or "id" for unique_id.
        """
        mGene = "Manual-" + gene
        if self.getNodeId(_arg, _type) is None or self.getNodeId(mGene, "metacyc") is None:
            print("Unable to delete this association the gene or the reaction"
                  + " doesn't exist.")
        else:
            reacId = str(self.getNodeId(_arg, _type)[0])
            gNodeId = str(self.getNodeId(mGene, "metacyc")[0])
            # In this case, there is only one association, so the gene will
            # delete.
            if len(self.dicOfAssoc[gNodeId]) == 1:
                self.dicOfAssoc.pop(gNodeId)
                self.delNode(gNodeId, "id")
            else:
                # In this case, it deletes only the association and the
                # suitable relation.
                for assoc in self.dicOfAssoc[gNodeId]:
                    if re.search(reacId, assoc[0]):
                        self.dicOfAssoc[gNodeId].remove(assoc)
                for rlt in self.getRelation(reacId, "out"):
                    if rlt.getIdIn() == int(gNodeId):
                        self._delRelation(rlt)
                        
            
#==============================================================================
# manipulating de novo node:     
#==============================================================================
    
    def _basicNode(self, _class):
        """
        Return a new id. This id will start with the species tag (ex: Tiso)
        to disting it from tgdbref's id. Tag is defined in parameters
        Also generate an empty node with only the class
        Input:  
            _class: the class of node (ex: reaction)
        Output: 
            (newId,<newNode>)
        """
        #check if the class is define in the policy
        if _class in self.getPolicy().getClassOfNode():
            #define a new unique_id:
            #generator of the int part of ids that contains the species tag
            novoNodeId = [int(node_id.replace(para.species,"")) 
            for node_id in self.getDicOfNode().iterkeys() 
            if para.species in node_id]
            novoNodeId.sort()
            try:
                #novoNodeId is not empty, recovere the max id to define the newId
                maxId = novoNodeId[-1]
                _id = para.species+str(maxId+1)
            except IndexError:
                #novoNodeId is empty, create the first specie specific id
               _id = para.species+"1"
            newNode = Node([_class,_id])
            return(_id,newNode)
        else:
            raise TypeError("the type of class given is not define in the policy")

    def createNode(self,_class,dicOfMisc,listOfRelation = None):
        """
        Creation of new node to add in the network.
        Input:
            _class <str>: class of node (gene, reaction...)
            dicOfMisc <dict>: dictionnary of miscellious data
            listOfRelation <list>: list of list of data representing the data for relation.
        Output:
            (newNodeId,<node>)
        """
        (newId,newNode) = self._basicNode(_class)
        #add the new node in the tgdbp
        newNode.misc = dicOfMisc
        self._addNode(newNode)
        if listOfRelation is not None:
            for _data in listOfRelation:
                try:
                    #'_self' in a relation is where to put the id of the current new node (if needed)
                    selfIndex = _data.index("_self")
                    _data[selfIndex] = newId
                except ValueError:
                    pass
                newRelation = Relation(_data)
                self._addRelation(newRelation)

        return (newId,newNode)

    def createEntry(self, _data, metacycTgdb, association = ""):
        """
        CreateEntry() allows to dispatch the different types of data to
        create the appropriate entry. the _data is a list of information 
        about the entry (from dataToUpdate.ods). The index 0 is always the 
        type of entry (reaction, compound, patwhay, protein).
        Input:  _data <list> _data correspond to a line of dataToUpdate.ods
               metacycTgdb: <tgdb> metacyc tgdb 
        """
        category, commonName, ref, formula, pathways = _data
        listOfCname = commonName.split(";")
        ref = ref.split(";")
        # recover the pathways associated to this entry
        if len(pathways) != 0:
            listOfPath = pathways.split(";")
        else:
            listOfPath = None

        if category == "reaction":
            rev = re.compile("<=>")
            leToRi = re.compile("=>")
            riToLe = re.compile("<=")
            if (len(rev.findall(formula)) == 1):
                direction = "REVERSIBLE"
            elif (len(leToRi.findall(formula)) == 1):
                direction = "LEFT-TO-RIGHT"
            elif (len(riToLe.findall(formula)) == 1):
                direction = "RIGHT-TO-LEFT"
            else:
                raise TypeError("direction not defined in formula, check the "
                                + "readme, need '=>', '<=>', or '<='.")
            #separate the left and right of the formula
            formulaL,formulaR = formula.split("=")
            #exprReg will recover compound and stochio
            #from a formula like 'X [Meta1] + Y [Meta2] => Z [Meta3]                
            exprReg = re.compile('(?P<stoech>[0-9.]+)\s+\[(?P<metabo>[\w\-]+)\]')
            # Generator of dictionary, key = stoech,metabo
            # value = the stoechiometry and the metabo name.
            leftG = (gpr.groupdict() for gpr in exprReg.finditer(formulaL))
            rightG = (gpr.groupdict() for gpr in exprReg.finditer(formulaR))
            leftCompound = []
            rightCompound = []
            for d in leftG:
                leftCompound.append((d['metabo'],d['stoech']))
                #check if the current metabo is in the current network
                if self.getNodeId(d['metabo']) is not None or self.getNodeId(d['metabo'],"cname") is not None:
                     pass
                # Check if the current metabo is in metacyc, match by
                # metacyc_id.
                elif metacycTgdb.getNodeId(d['metabo']) is not None:
                     self._copyNodeExtend(metacycTgdb,
                                          metacycTgdb.getNodeId(d['metabo'])[0])
                else:
                    message = "Unknown metabolite: "+str(d['metabo'])+ " Not "
                    message += "found in the network or in full metacyc"
                    print("%s" %message)
                    return False
            for d in rightG:
                rightCompound.append((d['metabo'],d['stoech']))
                if self.getNodeId(d['metabo']) is not None or self.getNodeId(d['metabo'],"cname") is not None:
                     pass
                elif metacycTgdb.getNodeId(d['metabo']) is not None:
                     self._copyNodeExtend(metacycTgdb,
                                          metacycTgdb.getNodeId(d['metabo']))
                else:
                    message = "Unknown metabolite: "+str(d['metabo'])+ " Not "
                    message += "found in the network or in metacyc"
                    print("%s" %message)
                    return False
                
            reacId = self.createReaction(listOfCname, ref, leftCompound,
                                         rightCompound, direction, listOfPath)
            # It adds an association, if it exists.
            if association:
                info = association.split(";")
                if re.search("gene", info[0]):
                    reacId, reacNode = self.getNodeId(reacId, "id")
                    reacMeta = reacNode.getMisc()["metacyc_id"]
                    self.addAssociation(info[1], "MANUAL", str(reacMeta[0]))
            
        elif category == "compound":
            self.createCompound(listOfCname,ref) 
            
        elif category == "pathway":
            self.createPathway(listOfCname,ref,listOfPath)
            
        elif category == "protein":
            self.createProtein(listOfCname,ref,listOfTupleRHMM)

        elif category == "gene":
            self.createGene(listOfCname, ref, listOfTupleAssoc)
        
        else:
            raise TypeError("Wrong category, please refere to the ReadMe")
