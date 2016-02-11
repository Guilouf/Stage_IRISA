# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 11:12:10 2016

@author: maite
updateV2
"""

from datetime import date
import os
import collections
import sys


from lib.tinygraphdb import Tinygraphdb
from lib.tinygraphdbplus import Tinygraphdbplus

try:
    from pyexcel_ods3 import ODSBook,ODSWriter
except:
    print("package pyexcel-ods3 needed, use this cmd:\n pip install pyexcel-ods3")
    exit()
try:
    import docopt
except ImportError:
    print("package docopt needed, use this cmd:\n pip install "
          + "docopt")
    exit()

def main():
    args = docopt.docopt(__doc__)
    verbose = args["-v"]
    tgdbp_file_name = args["--tgdbp_file_name"]    
    tgdbRef_file_name = args["--tgdbRef_file_name"]
    data_to_update_file = args["--data_to_update_file"]
    update_history_file = args["--update_history_file"]

    #I/From manual_update:
    #1/ read manual_update and manual_update_history
    #2/ parse manual_update to 4 list_of_data
    #3/ update tgdbp
    #4/ update manual_update_history

    #II/From manual_update_history:
    #1/ read manual_update_history
    #2/ parse manua_update_history to come back to a specific version
    #3/ update tgdbp
    #4/ create a copy of manual_update_history with new info

def read_ods(ods_file):
    book = ODSBook(ods_file)
    dic_of_sheets = book.sheets()
    return dic_of_sheets

def parse_dic_of_sheets(dic_of_data_to_update):

    try:
        sheet_entry_to_delete = dic_of_data_to_update["entryToDelete"]
    except KeyError:
        message = "Can not find sheet 'entryToDelete' in dataToUpdate, please "
        message += "check the file or the given argument..."
        print("%s" %message)
        exit()

    try:
        sheet_entry_to_add = dic_of_data_to_update["entryToAdd"]
    except KeyError:
        message = "Can not find sheet 'entryAdded' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

    try:
        sheet_entry_to_create = dic_of_data_to_update["entryToCreate"]
    except KeyError:
        message = "Can not find sheet 'entryCreated' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

    try:
        sheet_entry_to_update = dic_of_data_to_update["entryToUpdate"]
    except KeyError:
        message = "Can not find sheet 'entryUpdated' in dataToUpdate, "
        message += "please check the file or the given argument..."
        print("%s" %message)
        exit()

    #ToDelete
    #create a list that contains the tgdbp_id of entry to delete
    #Start to recover the id at the 2nd line, the first corresponding to the header 
    entry_to_delete = [line for line in sheet_entry_to_delete
    if sheet_entry_to_delete.index(line) >= 1
    and len(line[0]) != 0]
    
    #entryToAdd
    #create a generator that contains the tgdbp_id of entry to add
    #Start to recover the id at the 2nd line, the first corresponding to the header 
    entry_to_add = [line for line in sheet_entry_to_add
    if sheet_entry_to_add.index(line) >= 1
    and len(line[0]) != 0]
    
    #entryToCreate
    #create a generator that contains the data of entry to create and add
    #Start to recover the id at the 2rd line, the first corresponding to the header 
    entry_to_create = [line for line in sheet_entry_to_create
    if sheet_entry_to_create.index(line) >= 1
    and len(line[0]) != 0]
    
    #entryToUpdate
    #create a generator that contains the metacyc_id of entry to validate
    #Start to recover the id at the 2nd line, the first corresponding to the header 
    entry_to_update = [line for line in sheet_entry_to_update
    if sheet_entry_to_update.index(line) >= 1
    and len(line[0]) != 0]
    
    return (entry_to_delete,entry_to_add,entry_to_create,entry_to_update)

def update_tgdbp(data_to_update,tgdbp,history_file,version):
    
    
def add_history(sheets_update,history_file,version):
    read_ods(history_file)

a = read_ods("template_DataToUpdate.ods")
b = parse_update_file(a)