[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
# Stage_IRISA
Scripts et BDD sur la reconstruction de metagénomes bacteriens pour la production de vitamines
à l'aide de la programmation logiques ASP

# Sample data
Pre-downloaded databases, results, figures.. can be found at this [link](https://drive.google.com/drive/folders/0B4c604_XLW5tTzBkTkYyQTFDazg?usp=sharing).

# Prerequisites

- Python 3.5


    >All presented modules can downloaded and installed using pip
    (`pip install -r path/to/Stage_IRISA/requirement.txt --user`) for installing all modules
    or (`pip install module_name --user`) for installing modules one by one
 

- Pyasp: A binding between ASP and python. Can be tricky with windows, the path in the module
 leading to gringo and clasp may have to be hardcoded if problems appears.
 This module contains the binary of gringo(v4) and clasp
- Biopython, library used to download and parse GenBank annotation files
- Matplotlib, used to draw the heatmap style table
- Numpy, used to handle matrices
- sqlalchemy, the libary that provides the ORM for data storage
    
> Some modules are not described here because they are provided in all python 3.5 distribution

# First launch
This project can be split in two parts:
One for retrieving the data, and the other to process data.
Here we will see the procedure to retrieve the data needed for the programm.



## The "ListAccess" file 
consist as a text file containing at each line an NCBI [ accession number. ](http://www.ncbi.nlm.nih.gov/Sequin/acc.html)
The format is strict, an error will be raised if not respected

This file have to be filed by the user with the desired accession numbers, and will be used
by the script.

The script can handle accession numbers from NCBI master records, Whole Genome Shotgun and 
obviously complete genomes


## Data download procedure
- Recup??ec script will access to the `ListAccess` file, and automatically download the data from
the NCBI Nucleotide database. Data are saved in the ORM file, but yet not translated into
ASP facts.

> If there is network problems, an alternative method is available: When running the script, add 
as a commandline argument the path to a genbank file, with this format: `/path/_bacterianame.gb`

- Once the `Recup_EC_num` have been successfully executed, launching `bddbis` will translate
the data into ASP facts

# Data analysis with ASP
A single script, `asp_script`, handle all the tasks for the processing with ASP.
This script has several different commandline arguments, that does not have to be written in
a particular order or does not have to be all present

## Selecting questions
- Question1: Which bacteria can produce on their own which vitamin?
- Question2: Which bacteria that cannot produce a vitamin can cooperate with another to produce
a vitamin?
- Question3: Which bacteria can cooperate to produce all the vitamins?

- Argument `Q1_2`: Running the script with this argument will produce a result table for
both the question 1 and 2 in the folder `ASP/Output`. Because the script can run question2 only
for one vitamin, a prompt will appear asking which vitamin to select. An error in typing will
lead of an absence of solutions for the question 2.

- Argument `Q3`: The script will run the question3


> !! Typing the arguments `Q1_2` and `Q3` will not raise errors but leads to false results !!
 => Juste one question per run


## Other options
- `heatable` argument: Enable the view of an heatmap style table, work with all questions.
It also outputs in `ASP/Ouput` csv tables to summarize the heamap view, named like `tab_csv_vitXX.csv`
- `show_asp` argument: Enable in the standard output the output of clasp

# TODO
- [ ] Title for the heatmap tables
- [ ] Caption for the numbers in tables
- [x] Add EC_uni and other heavy stuff in google drive or other
- [ ] Update to metacyc 20
- [ ] Setup to auto install modules
- [ ] Refactor module and class names

# Cheat
- `gringo file | clasp` to test ASP separately
- var in CAPS, const in lowercase..
