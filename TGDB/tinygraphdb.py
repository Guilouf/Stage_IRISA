# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:58:12 2015
Version: 1.0.3 - 25-01-16
@author: Meziane AITE, meziane.aite@inria.fr
Tinygraphdb is an object representing a metabolic network.
TGDB is define by a <Policy>, a dictionnary of <Node> and a tuple of <Relation>
The policy define the way Node and Relation are associated
A node is an Object that contains information about an element of the network 
(can be a pathway, reaction...).
A realtion defines how two nodes are connected

TGDB format is used to stock and manipulate a database of metabolic network. Work more like
a database than a metabolic network. The format used to manipulate a metabolic network is the tgdbp.

"""

from policy import *
from node import *
from relation import *
import parameters as para
import collections
try:
    from pyexcel_ods3 import ODSWriter
except:
    print("package pyexcel-ods needed, use this cmd:\n pip install pyexcel-ods3")
    exit()

class Tinygraphdb:
    def __init__(self,tgdbFilePath = None):
        """
        tgdbFilePath: path of the file .tgdb
        if None, initialise an empty <Tinygraphdb>
        """
        if tgdbFilePath is not None:        
            with open(tgdbFilePath,'r') as f:        
                tgdbInArray = f.readlines()
            self.copyPolicy(tgdbInArray)
            self.copyGraph(tgdbInArray)
            
        else:
            self.tuplOfRelation = ()
            self.dicOfNode = {}
            self.policy = Policy()
            self.dbNotes = {}
#==============================================================================
# Constructor / getter            
#==============================================================================
        
    def setDBNotes(self,dicOfDB):
        """
        #dbNotes: dictionnary recovering informations about the DBs used.
        {"metacyc":{version:XX,...},"ecocyc":{...}...}
        """
        if type(dicOfDB) is dict:
            self.dbNotes = dicOfDB
            return True
        else: 
            return False
        
    def getDBNotes(self):
        return self.dbNotes

    def copyPolicy(self,_from):
        """
        allow to copy the policy of a tgdb stored in a list (ex after reading a .tgdb with an readlines())
        input: tgdbpInArray <list>
        OR copy the policy from a <Tinygraphdb> object
        input: tgdb <Tinygraphdb>
        """
        if type(_from) is list:
            self.policy = Policy(_from)
        else:
            self.policy = _from.getPolicy()
        
        
    def getPolicy(self):
        return self.policy
    
    def copyGraph(self,tgdbInArray):
        """
        Allow to recover all the informations of the tgdb file stored in a list.
        stock all the nodes in a dictionnary "self.dicOfNode", key = node id / value = node object
        stock all the relations in a tuple "self.tuplOfRelation"
        Input: tgdbInArray <list>
        """
        self.dicOfNode = {}
        self.dbNotes = {}
        listOfRelation = []
        try:
            dbIndex = tgdbInArray.index("Data Base informations\n")
        except ValueError:
            pass
        #Index where start Nodes
        nodeIndex = tgdbInArray.index("Nodes\n")
        #Index where start Relations       
        relationIndex = tgdbInArray.index("Relations\n")
        
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
        for line in tgdbInArray[nodeIndex+1:relationIndex] if line != "\n"]
        #
        for data in nodeSection:
            #Create a new Node object (cf node.py)                
            node = Node(data) 
            #add the node into the dictionnay
            self.dicOfNode[node.getId()] = node 

        # generator of data to input in Relation()
        relationSection = (line.replace("\n","").split("\t") 
        for line in tgdbInArray[relationIndex+1:len(tgdbInArray)] if line != "\n")
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

    def generateFile(self, fileName = "newTGDB.tgdb"):
        """
        Allow to create a file tgdb to stock all the data.
        Input: fileName <string> the file name where to stock the output
        Output: file .tgdb
        """
        # Order the dictionary of node by unique id and the tuple of relation
        # by the node in id.
        dicKeys = self.getDicOfNode().keys()
        dicKeys.sort()
        orderedTuplOfRelation = tuple(sorted(self.tuplOfRelation,
                                           key=lambda x: x.idIn, reverse=False))
        with open(fileName,'w') as f:
            f.write("Data Base informations\n")
            for dbName,data in self.getDBNotes().iteritems():
                f.write(dbName+":\n")
                for k,v in data.iteritems():
                   f.write("\t"+k+":"+v+"\n")
            f.write("\n")
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

    def getAllData(self,metacycVersion): 
        """
        Allow to recovere all the pathways, reactions and compounds in differents sheets.
        output: 
        #TODO TO UPDATE !!!
        """
        sheet_metacycPathways = [["metacyc_id","common_name and synonymous"]]
        sheet_metacycReactions = [["metacyc_id","common_name and synonymous"]]    
        sheet_metacycMetabolites = [["metacyc_id","common_name and synonymous"]]
        sheet_metacycReferences = []
        
        #create a generator of pathways, reactions, metabolites and References
        metaboliteID = (rlt.getIdOut()for rlt in self.getTuplOfRelation()
        if rlt.getType() == "has lef"
        or rlt.getType() == "has right")
   
        pathwayID = (k for k,n in self.getDicOfNode().iteritems()
        if n.getClass() == "pathway")
    
        reactionID = (k for k,n in self.getDicOfNode().iteritems()
        if n.getClass() == "reaction")
            
        references = (node.getMisc()["db"][0] for node in self.getDicOfNode().values()
        if node.getClass() == "xref")
        
        #To avoid repetitions, need to convert to a set
        print("creating set Of metabolites ...\n")
        setMetaboliteID = set()
        for m in metaboliteID:
            setMetaboliteID.add(m)
        print("Done.\n")
    
        print("creating set Of pathways ...\n")
        setPathwayID = set()
        for p in pathwayID:
            setPathwayID.add(p)
        print("Done.\n")
        
        print("creating set Of reactions ...\n")
        setReactionID = set()
        for r in reactionID:
            setReactionID.add(r)
        print("Done.\n")
    
        print("creating set Of references ...\n")
        setReferences = set()
        for r in references:
            setReferences.add(r)
        print("Done.\n")
    
        print("recovering all metabolites...\n")
        count = 1
        for m in setMetaboliteID:
            print("Metabolite "+str(count)+"/"+str(len(setMetaboliteID)))
            metacyc_id = self.getDicOfNode()[m].getMisc()["metacyc_id"][0]
            try:
                cnames = self.getDicOfNode()[m].getMisc()["common_name"]
                for name in cnames:
                    sheet_metacycMetabolites.append([str(metacyc_id),str(name)])
            except KeyError:
                cnames = None
                
            try:
                synonyms = (self.getDicOfNode()[rlt.getIdOut()].getMisc()["label"][0] for rlt in self.getRelation(m,"in")
                if rlt.getType() == "has name")
                for syn in synonyms:
                    sheet_metacycMetabolites.append([str(metacyc_id),str(syn)])
            except TypeError:
                pass
            count += 1
    
        print("\nRecovering all reactions...\n")
        count = 1
        for r in setReactionID:
            print("Reaction "+str(count)+"/"+str(len(setReactionID)))
            metacyc_id = self.getDicOfNode()[r].getMisc()["metacyc_id"][0]
            try:
                cnames = self.getDicOfNode()[r].getMisc()["common_name"]
                for name in cnames:
                    sheet_metacycReactions.append([str(metacyc_id),str(name)])
            except KeyError:
                cnames = None

            try:
                synonyms = (self.getDicOfNode()[rlt.getIdOut()].getMisc()["label"][0] for rlt in self.getRelation(r,"in")
                if rlt.getType() == "has name")
                for syn in synonyms:
                    sheet_metacycReactions.append([str(metacyc_id),str(syn)])
            except TypeError:
                pass
            count += 1
    
        print("\nRecovering all pathways...\n")
        count = 1
        for p in setPathwayID:
            print("Pathway "+str(count)+"/"+str(len(setPathwayID)))
            metacyc_id = self.getDicOfNode()[p].getMisc()["metacyc_id"][0]
            try:
                cnames = self.getDicOfNode()[p].getMisc()["common_name"]
                for name in cnames:
                    sheet_metacycPathways.append([str(metacyc_id),str(name)])
            except KeyError:
                cnames = None

            try:
                synonyms = (self.getDicOfNode()[rlt.getIdOut()].getMisc()["label"][0] for rlt in self.getRelation(p,"in")
                if rlt.getType() == "has name")
                for syn in synonyms:
                    sheet_metacycPathways.append([str(metacyc_id),str(syn)])
            except TypeError:
                pass
            count += 1
    
        print("\nRecovering all references...\n")
        count = 1        
        for r in setReferences:
            print("Reference "+str(count)+"/"+str(len(setReferences)))
            sheet_metacycReferences.append([str(r)])
            count += 1
    
        data = collections.OrderedDict()
        data["metacycPathways"] = sheet_metacycPathways 
        data["metacycReactions"] = sheet_metacycReactions
        data["metacycMetabolites"] = sheet_metacycMetabolites
        data["metacycReferences"] = sheet_metacycReferences
        fileName = para.allMetacycData.replace("XX",metacycVersion)
        writer = ODSWriter(fileName)
        writer.write(data)
        writer.close()
    
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
            
#==============================================================================
# For Relations:     
#==============================================================================

    def getRelation(self,_id,_dir="in"):
        """
        getRelation allow to recover from a node id, all the relations where this id is 'In'
        input: _id <string> the unique id
                _dir <string> the position of the node in the relation "in" or "out"
        output: tuple of object 'Relation' cf relation.py 
                None: there is no relation FROM the id given 
        """   
        tmpListRelation=[]
        for rlt in self.getTuplOfRelation():
            if rlt.getIdIn() == _id and _dir == "in":
                tmpListRelation.append(rlt)
            if rlt.getIdOut() == _id and _dir == "out":
                tmpListRelation.append(rlt)
        if len(tmpListRelation) == 0:
            return None
        else:
            rez = tuple(tmpListRelation)
            return rez    

