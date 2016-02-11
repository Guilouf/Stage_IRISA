# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:53:35 2015
Version: 1.0.3 - 08-02-16
@author: Meziane AITE, meziane.aite@inria.fr
Define a relation in tgdb object.
Input: 
    data_in_array <array>: corresponding to a relation line of a tgdb file.
                        [id_in,type,id_out,miscellious...]

Output:
    Create a class Relation
"""

class Relation:
    def __init__(self,data_in_array):
        self.id_in = data_in_array[0]
        self.type = data_in_array[1]
        self.id_out = data_in_array[2]
        self.misc = {}
        if len(data_in_array) > 3:
            i = 3
            while (i+1) < len(data_in_array): 
                #in case diff information for the same key               
                if data_in_array[i] not in self.misc.keys():
                    self.misc[data_in_array[i]] = [data_in_array[i+1]]    
                else:
                    self.misc[data_in_array[i]].append(data_in_array[i+1])
                i+=2

    def getIdIn(self):
        # idIn is an int type that contains the id In
        return(self.id_in)

    def getType(self):
        # type is an string type that contains the type of relation.
        return(self.type)

    def getIdOut(self):
        # idOut is an int type that contains the id Out
        return(self.id_out)

    def getMisc(self):
        # misc is a dictionary type that contains the type of
        # misc info as key and the data as value
        return(self.misc)        

    def toString(self):
        line = str(self.getIdIn())+"\t"+str(self.getType())+"\t"+str(self.getIdOut())
        if len(self.getMisc()) != 0:
            for k,n in self.getMisc().iteritems():
                if len(n) == 1:
                    line = line+"\t"+str(k)+"\t"+str(n[0])
                else:
                    for i in range(len(n)):
                        line = line + "\t"+str(k)+"\t"+str(n[i])
        return line
    
    def compare(self,relation):
        if (relation.getIdIn() == self.getIdIn() and relation.getType() == self.getType() 
        and relation.getIdOut() == self.getIdOut()):
            return True
        else:
            return False
                        