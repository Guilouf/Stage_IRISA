# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:57:12 2015
Version: 1.0 - 27-07-15
@author: Meziane AITE, meziane.aite@inria.fr
"""

from lib.tinygraphdb import Tinygraphdb
from lib.tinygraphdbplus import Tinygraphdbplus

from datetime import date
import os
import collections
import sys
try:
    from pyexcel_ods3 import ODSBook,ODSWriter
except:
    print("package pyexcel-ods3 needed, use this cmd:\n pip install pyexcel-ods3")
    exit()

#Globals variables imported from parameters.py
import parameters as para

print("\n############################################################\n")  
print("step 0/5: Parsing and checking arguments")
print("\n############################################################\n") 
verbose = False
try:
    if sys.argv[1] == "-v":
        verbose = True
except IndexError:
    pass
tgdbp_file_name = "test"    
tgdbRef_file_name = "test"
data_to_update_file = "test"
manual_update_history_file = "test"
print("\n############################################################\n")  
print("step 1/5: Loading tgdbRef.tgdb and current network tgdbp")
print("\n############################################################\n") 

try:
    # Twice, oldTgdbp will serve as reference for wikiUpdate
    old_tgdbp = Tinygraphdbplus(tgdbp_file_name)
    current_tgdbp = Tinygraphdbplus(tgdbp_file_name)
    if verbose: print("tgdbp successfully loaded.")
except:
    print("can not load the curruent tgdbp file")
    exit()

try:
    tgdb_ref = Tinygraphdb(tgdbRef_file_name)
    if verbose: print("tgdbRef successfully loaded.\n")
except:
    print("Can not load the tgdbRef file")
    exit()


print("\n############################################################\n")  
print("step 2/5: Parsing dataToUpdate file")
print("\n############################################################\n") 

# loading dataToUpdateFile as a dictionary
book = ODSBook(data_to_update_file)
dic_of_data_to_update = book.sheets()

# 2 case: if the file is the native dataToUpdate.ods or if its
# manualUpdateHistory.ods.
try:
    sheet_entry_to_delete = dic_of_data_to_update["entryToDelete"]
except KeyError:
    try:
        sheet_entry_to_delete = dic_of_data_to_update["entryDeleted"]
    except KeyError:
        message = "Can not find sheet 'entryToDelete' in dataToUpdate, please "
        message += "check the file or the given argument..."
        print("%s" %message)
        exit()

try:
    sheet_entry_to_add = dic_of_data_to_update["entryToAdd"]
except KeyError:
    try:
        sheet_entry_to_add = dic_of_data_to_update["entryAdded"]
    except KeyError:
        message = "Can not find sheet 'entryAdded' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

try:
    sheet_entry_to_create = dic_of_data_to_update["entryToCreate"]
except KeyError:
    try:
        sheet_entry_to_create = dic_of_data_to_update["entryCreated"]
    except KeyError:
        message = "Can not find sheet 'entryCreated' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

try:
    sheet_entry_to_update = dic_of_data_to_update["entryToUpdate"]
except KeyError:
    try:
        sheet_entry_to_update = dic_of_data_to_update["entryUpdated"]
    except KeyError:
        message = "Can not find sheet 'entryUpdated' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

#ToDelete
#create a generator that contains the tgdbp_id of entry to delete
#Start to recover the id at the 2nd line, the first corresponding to the header 
entry_to_delete = (line for line in sheet_entry_to_delete
if sheet_entry_to_delete.index(line) >= 1
and len(line[0]) != 0)
    
#entryToAdd
#create a generator that contains the tgdbp_id of entry to add
#Start to recover the id at the 2nd line, the first corresponding to the header 
entry_to_add = (line for line in sheet_entry_to_add
if sheet_entry_to_add.index(line) >= 1
and len(line[0]) != 0)

#entryToCreate
#create a generator that contains the data of entry to create and add
#Start to recover the id at the 2rd line, the first corresponding to the header 
entry_to_create = (line for line in sheet_entry_to_create
if sheet_entry_to_create.index(line) >= 1
and len(line[0]) != 0)

#entryToUpdate
#create a generator that contains the metacyc_id of entry to validate
#Start to recover the id at the 2nd line, the first corresponding to the header 
entry_to_update = (line for line in sheet_entry_to_update
if sheet_entry_to_update.index(line) >= 1
and len(line[0]) != 0)

print("\n############################################################\n")  
print("Step 3/5: Updating the current tgdbp and manualUpdateHistory")
print("\n############################################################\n") 

#define the today date
_date = date.today()
#Define the current and new tgdbp version
try:
    current_tgdbp_version = float(tgdbp_file_name.split("_")[1].split(".tgdbp")[0])
    new_version = current_tgdbp_version + 0.1
    new_tgdbp_name = tgdbp_file_name.split("_")[0]+str(new_version)+".tgdbp"
except IndexError:
    current_tgdbp_version = 0.9
    new_version = current_tgdbp_version + 0.1
    new_tgdbp_name = tgdbp_file_name.split(".tgdbp")[0]+"_"+str(new_version)+".tgdbp"

#Loading the manualUpdateHistory    
book = ODSBook(manual_update_history_file)
try:
    sheet_entry_deleted = book.sheets()["entryDeleted"]
except KeyError:
    print("Can not find sheet 'entryDeleted' in manualUpdateHistory file, please check the file or the given argument...")
    exit()
try:
    sheet_entry_added = book.sheets()["entryAdded"]
except KeyError:
    print("Can not find sheet 'entryAdded' in manualUpdateHistory file, please check the file or the given argument...")
    exit()
try:
    sheet_entry_created = book.sheets()["entryCreated"]
except KeyError:
    print("Can not find sheet 'entryCreated' in manualUpdateHistory file, please check the file or the given argument...")
    exit()

try:
    sheet_entry_updated = book.sheets()["entryUpdated"]
except KeyError:
    print("Can not find sheet 'entryUpdated' in manualUpdateHistory file, please check the file or the given argument...")
    exit()

# Updating the current tgdbp.

# To delete
_statement = False
print("\n")

print("Deleting entry...\n")
for line in to_delete:
    try:
        _id, remarks = _line
        print("\t"+str(_id)+"\n")
        current_tgdbp.delNode(str(_id),"id")
        # Update the current sheet
        ici
        #TODO finir
        newLine = line + [str(tgdb_ref_version), str(currentTgdbpVersion),
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
