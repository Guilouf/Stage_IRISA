# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:54:45 2015
Version: 1.0.3 - 08-02-16
@author: Meziane AITE, meziane.aite@inria.fr
Define a policy in tgdb or tgdbp object.
create a class policy that define the types of relations in a network.
Can be use for a TGDB or a TGDBP 

Input: 
    tgdb_in_array <array>: tgdb file converted to an array.

Output:
    Create a class Policy
"""

class Policy:
    """
    input: array, corresponding to an entire tgdb or tgdbp file put in an array with readlines()
    self.policyInArray is an array that contains all the type of relations.
        ex: [['reaction','is in pathway','pathway'],['pathway','has name','name']...]
    self.classOfNode is a set of the differents class of node
        ex: ('class','compound','gene'...)
    self.typeOfArc is dictionnary with key the class of node and the value, the relation in array
        ex: {'reaction':[['is in pathway','pathway'],['has right','compound']...]...}
    """

    def __init__(self,tgdb_in_array = None):
        self.policy_in_array = []
        self.class_of_node = set()
        self.type_of_arc = {}

        if tgdb_in_array is not None:
            policy_index = tgdb_in_array.index("Policy\n")
            nodes_index = tgdb_in_array.index("Nodes\n")
            for i in range(policy_index+1,nodes_index):
                line = tgdb_in_array[i]
                line = line.replace("\n","")
                if len(line) != 0:
                    line = line.split("\t")
                    self.policy_in_array.append(line)
                else:
                    break
            
            self._setClassOfNode()
            self._setTypeOfArc()
            
    def setPolicyInArray(self,array):
        #check array
        for i in array:
            if len(i) < 3:
                raise ValueError("Array given to set the PolicyInArray is uncorrect")
        self.policy_in_array = array
        self._setClassOfNode()
        self._setTypeOfArc()

    def getPolicyInArray(self):
        return self.policy_in_array
            
    def _setClassOfNode(self):
        if len(self.policy_in_array) != 0:
            for line in self.policy_in_array:
                self.class_of_node.add(line[0])
                self.class_of_node.add(line[2])
        else:
            raise ValueError("PolicyInArray is not defined")

    def getClassOfNode(self):
        return self.class_of_node

    def _setTypeOfArc(self):
        """
        setTypeOfArc create a dictionnary of arc allowed in the policy. key: nodeIn / values: type of node and nodeOut
        """
        if len(self.class_of_node) != 0:
            for _class in self.class_of_node:
                self.type_of_arc[_class] = [] 
                
            for line in self.policy_in_array:
                arc = line[1:]
                self.type_of_arc[line[0]].append(arc)
        else:
            raise ValueError("PolicyInArray and/or classOfNode are not defined")
            
    def getTypeOfArc(self):
        return(self.type_of_arc)

