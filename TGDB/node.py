# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:53:13 2015
Version: 1.0.3 - 08-02-16
@author: Meziane AITE, meziane.aite@inria.fr
Define a node in tgdb object.
Input: 
    data_in_array <array>: corresponding to a node line of a tgdb file.
                        [class,id,miscellious...]
Output:
    Create a class Node
"""

class Node:
    def __init__(self,data_in_array):
        self._class = data_in_array[0]
        self._id = data_in_array[1]
        self.misc = {}
        if len(data_in_array) > 2:
            i = 2
            #add the misc data in a dict
            while (i+1) < len(data_in_array): 
                #in case diff information for the same key               
                if data_in_array[i] not in self.misc.keys():
                    self.misc[data_in_array[i]] = [data_in_array[i+1]]    
                else:
                    self.misc[data_in_array[i]].append(data_in_array[i+1])
                i += 2
                
    def getClass(self):
        #_class is a string type that contains the type of node
        return(self._class)

    def getId(self):
        # _id is an int type that contains the unique id of the node
        return(self._id)

    def getMisc(self):
        #misc is a dictionary type that contains the type of misc info as key and the data as value
        return(self.misc)        
    
    def toString(self):
        line = str(self.getClass())+"\t"+str(self.getId())
        if len(self.getMisc()) != 0:
            for k,n in self.getMisc().iteritems():
                if len(n) == 1:
                    line = line+"\t"+str(k)+"\t"+str(n[0])
                else:
                    for i in range(len(n)):
                        line = line + "\t"+str(k)+"\t"+str(n[i])
        return line