# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:57:12 2015
Version: 1.0 - 27-07-15
@author: Meziane AITE, meziane.aite@inria.fr
"""

from lib.tinygraphdb import Tinygraphdb
from lib.tinygraphdbplus import Tinygraphdbplus
from lib.wikiGenerator import *
from lib.sbmlGenerator import *
from datetime import date
import os
import collections
try:
    from pyexcel_ods3 import ODSBook,ODSWriter
except:
    print("package pyexcel-ods3 needed, use this cmd:\n pip install pyexcel-ods3")
    exit()
#Globals variables imported from parameters.py
import parameters as para


#
print("\n############################################################\n")  
print("step 1/5: Loading metacyc.tgdb and current network tgdbp files")
print("\n############################################################\n") 

try:
    # Twice, oldTgdbp will serve as reference for wikiUpdate
    oldTgdbp = Tinygraphdbplus(para.currentTgdbpFile)
    currentTgdbp = Tinygraphdbplus(para.currentTgdbpFile)
    print("current tgdb successfully loaded.\n")
except:
    print("can not load the curruent tgdbp file")
    exit()

try:
    metacycTgdb = Tinygraphdb(para.metacycTgdbFile)
    print("Metacyc tgdb successfully loaded.\n")
except:
    print("Can not load the metacyc tgdb file")
    exit()


print("\n############################################################\n")  
print("step 2/5: Parsing dataToUpdate file")
print("\n############################################################\n") 

# loading dataToUpdateFile as a dictionary
book = ODSBook(para.dataToUpdateFile)
dicOfDataToUpdate = book.sheets()

# 2 case: if the file is the native dataToUpdate.ods or if its
# manualUpdateHistory.ods.
try:
    sheet_entryToDelete = dicOfDataToUpdate["entryToDelete"]
except KeyError:
    try:
        sheet_entryToDelete = dicOfDataToUpdate["entryDeleted"]
    except KeyError:
        message = "Can not find sheet 'entryToDelete' in dataToUpdate, please "
        message += "check the file or the given argument..."
        print("%s" %message)
        exit()

try:
    sheet_metacycToAdd = dicOfDataToUpdate["metacycEntryToAdd"]
except KeyError:
    try:
        sheet_entryToDelete = dicOfDataToUpdate["metacycEntryAdded"]
    except KeyError:
        message = "Can not find sheet 'metacycEntryAdded' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

try:
    sheet_nonMetacycToAdd = dicOfDataToUpdate["nonMetacycEntryToAdd"]
except KeyError:
    try:
        sheet_entryToDelete = dicOfDataToUpdate["nonMetacycEntryAdded"]
    except KeyError:
        message = "Can not find sheet 'nonMetacycEntryAdded' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

try:
    sheet_entryToUpdate = dicOfDataToUpdate["entryToUpdate"]
except KeyError:
    try:
        sheet_entryToDelete = dicOfDataToUpdate["entryUpdated"]
    except KeyError:
        message = "Can not find sheet 'entryUpdated' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

#ToDelete
#create a generator that contains the metacyc_id of entry to delete
#Start to recover the id at the 2nd line, the first corresponding to the header 
toDelete = (line for line in sheet_entryToDelete
if sheet_entryToDelete.index(line) >= 1
and len(line[0]) != 0)
    
#metacycToAdd
#create a generator that contains the metacyc_id of entry to add
#Start to recover the id at the 2nd line, the first corresponding to the header 
metacycToAdd = (line for line in sheet_metacycToAdd
if sheet_metacycToAdd.index(line) >= 1
and len(line[0]) != 0)

#nonMetacycToAdd
#create a generator that contains the data of non-metacyc entry to create and add
#Start to recover the id at the 3rd line, the first corresponding to the header 
nonMetacycToAdd = (line for line in sheet_nonMetacycToAdd
if sheet_nonMetacycToAdd.index(line) >= 1
and len(line[0]) != 0)

#entryToUpdate
#create a generator that contains the metacyc_id of entry to validate
#Start to recover the id at the 2nd line, the first corresponding to the header 
entryToUpdate = (line for line in sheet_entryToUpdate
if sheet_entryToUpdate.index(line) >= 1
and len(line[0]) != 0)

print("\n############################################################\n")  
print("Step 3/5: Updating the current tgdbp and manualUpdateHistory")
print("\n############################################################\n") 

#define the today date
_date = date.today()
#Define the current and new tgdbp version
currentTgdbpVersion = float(para.currentTgdbpVersion) 
newVersion = currentTgdbpVersion + 0.1
newTgdbpName = para.path_Resultats+str(para.species)+"_"+str(newVersion)+".tgdbp"

#Loading the manualUpdateHistory    
book = ODSBook(para.manualUpdateHistoryFile)
try:
    sheet_entryDeleted = book.sheets()["entryDeleted"]
except KeyError:
    print("Can not find sheet 'entryDeleted' in manualUpdateHistory file, please check the file or the given argument...")
    exit()
try:
    sheet_metacycEntryAdded = book.sheets()["metacycEntryAdded"]
except KeyError:
    print("Can not find sheet 'metacycEntryAdded' in manualUpdateHistory file, please check the file or the given argument...")
    exit()
try:
    sheet_nonMetacycEntryAdded = book.sheets()["nonMetacycEntryAdded"]
except KeyError:
    print("Can not find sheet 'nonMetacycEntryAdded' in manualUpdateHistory file, please check the file or the given argument...")
    exit()

try:
    sheet_entryUpdated = book.sheets()["entryUpdated"]
except KeyError:
    print("Can not find sheet 'entryUpdated' in manualUpdateHistory file, please check the file or the given argument...")
    exit()

# Updating the current tgdbp.

# To delete
_statement = False
print("\n")

print("Deleting entry...\n")
for _line in toDelete:
    try:
        metacyc_id, association, remarks = _line
        print("\t"+str(metacyc_id)+"\n")
        currentTgdbp.delNode(str(metacyc_id))
        # Update the current sheet
        newLine = _line+[str(para.metacycVersion), str(currentTgdbpVersion),
                         str(_date)]            
        sheet_entryDeleted.append(newLine)
        print("\t\tDone.\n")
        _statement = True
    except StopIteration:
        print("No entry to delete\n")   
    
#metacycToAdd
print("Adding metacyc entry...\n")
for _line in metacycToAdd:
    try:
        print(_line)
        metacyc_id, association, remarks = _line
        currentTgdbp.copyNode(metacycTgdb, str(metacyc_id), "metacyc",
                              str(association))
        #update the current sheet
        newLine = _line+[str(para.metacycVersion), str(currentTgdbpVersion),
                         str(_date)]            
        sheet_metacycEntryAdded.append(newLine)
        print("\t\tDone.\n")
        _statement = True
    except StopIteration:
        print("No metacyc entry to add\n")   
    
#nonMetacycToAdd
print("Adding non-Metacyc entry...\n")
for _line in nonMetacycToAdd:    
    try:        
        print("\tCreate and Add " + str(_line[1].split(";")[0])+"\n")
        currentTgdbp.createEntry(_line[:-2], metacycTgdb, _line[-2])
        print("\tCreated.\n")
        #update the current sheet
        newLine = _line+[str(para.metacycVersion), str(currentTgdbpVersion),
                         str(_date)]            
        sheet_nonMetacycEntryAdded.append(newLine)
        print("\tAdded.\n")
        print("\t\tDone.\n")
        _statement = True
    except StopIteration:
        print("No non-Metacyc entry to add\n")   

#entryToUpdate
print("Updating entry...\n")
for _line in entryToUpdate:    
    try:
        metacyc_id,_data,action,remarks = _line
        print("\tUpdating "+str(metacyc_id)+"\n")
        _data = tuple(_data.split(";"))
        currentTgdbp.updateNode(metacyc_id,"metacyc",_data,action) #TODO MAJ
        print("\tUpdated.\n")
        #update the current sheet
        newLine = _line+[str(para.metacycVersion), str(currentTgdbpVersion),
                         str(_date)]            
        sheet_entryUpdated.append(newLine)
        print("\t\tDone.\n")
        _statement = True
    except StopIteration:
        print("No entry to update\n")   

# Creating the new currentTgdbp and the new manualUpdateHistory.
if _statement:
    print("Update complete!\n")
    currentTgdbp.generateFile(newTgdbpName)
    print("The new tgdbp was generate succesfully in the path: "
          + newTgdbpName + ".\n")
    
    try:    
        data = collections.OrderedDict()
        data["entryDeleted"] = sheet_entryDeleted 
        data["metacycEntryAdded"] = sheet_metacycEntryAdded 
        data["nonMetacycEntryAdded"] = sheet_nonMetacycEntryAdded
        data["entryUpdated"] = sheet_entryUpdated
        writer = ODSWriter(para.manualUpdateHistoryFile)
        writer.write(data)
        writer.close()
        print("The new version of manualUpdateHistory was generate succesfully"
              + " in the current directory")
        print("as manualUpdateHistory.ods")
    except UnicodeEncodeError:
        print("Please avoid space in given data beacause of unicode encode "
              + "error...\nCan't Update History.\n")
        exit()
else:
    print("Error in the data given, nothing was updated...\nEND")
    exit()

print("\n############################################################\n")  
print("Step 4/5: Updating the wiki online")
print("\n############################################################\n") 

if para.wikiSite is not None:
    udWiki = raw_input("Update wiki ? 'y' or 'n': ") 
    if udWiki == 'y':
        tgdbToWiki(metacycTgdb,currentTgdbp,oldTgdbp)
        print("The wiki online is completely up to date !\n")
    elif udWiki == 'n':
        print("Warning: The wiki is not up to date, now.\n")
    else:
        print("just 'y' or 'n'...\n")
        print("Warning: The wiki is not up to date, now.\n")

else:
    print("No WikiSite specified in parameters.py, Pass.\n")

print("\n############################################################\n")  
print("Step 5/5: Creation of the new sbml")
print("\n############################################################\n") 

print("Creating the new SBML file...\n")
sbmlFileName = newTgdbpName.replace(".tgdbp",".sbml")
prefixe = para.species
tgdbpToSbml(newTgdbpName,sbmlFileName,prefixe)
print("\nSBML file created")

print("END. \n")
