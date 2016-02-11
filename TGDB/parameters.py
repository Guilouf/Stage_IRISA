# -*- coding: utf-8 -*-
"""
Created on Mon May 18 17:43:14 2015
Version: 1.0.1 - 20-12-15
@author: maite
Fr: Remplir correctement ce fichier est indispensable au bon fonctionnement 
du package.
Les variables globales comme le nom de l'espece d'interet ou le lien vers 
le wiki sont importees depuis ce fichier. 
Prenez le temps de bien verifier les donnees, les scripts se chargent du reste
"""

# Globals declarations:

# Name of the species, used as aliases
# Nom de l'espece (ou alias du reseau), peut etre n'importe quoi, mais est
# caracteristique du reseau
# NB: evitez les espaces et caracteres speciaux
species = "WEN"

# nom complet de l'espece, utilise pour la creation des pages wiki
# Full name of the species
fullSpeciesName = "Wenelen"

# path directory of resultats and specific_files
# chemins d'acces des dossiers resultats et specific_files
# specifici_files: Seront stockes les fichiers propre au reseau actuel
# assoc_full, assoc_HMM, metacycXX.tgdb, le tgdbp de travail, les
# fichiers dataToUpdate.ods et l'historique.ods.
# Resultats: Seront stockes les fichiers cree a partir du reseau.
path_Resultats = "../resultats"+species+"/"
path_SpecificFiles = "../specific_files"+species+"/"

# dataToUpdate.ods contains 4 sheets (entryToDelete, metacycEntryToAdd,
# nonMetacycEntryToAdd and entryToValidate)
# dataToUpdate.ods est le fichier ods contenant les informations a mettre a
# jour dans le reseau.
# il est utilise dans le script networkUpdater.py qui le parsera pour
# ensuite appliquer ces MAJ sur le tgdbp il est important de ne jamais
# modifier la structure de ce fichier (nombre, ordre des colonnes, noms des
# feuilles)
# S'il est vraiment necessaire de le modifier, penser a prendre en compte
# ces modification dans networkUpdater.py , section 'parsing dataToUpdate'
# ET penser a modifier manualUpdateHistory.ods ansi que sa creation dans
# le networkUpdater.py ...
dataToUpdateFile = path_SpecificFiles+species+"_dataToUpdate.ods"

# the file containing all the history of manual updates manualUpdateHistory
# est le fichier ou sont stockees toutes les modifications du reseau actuel
# depuis la V1.0.
# Peut etre reutiliser comme un dataToUpdate pour une regeneration de reseau,
# ne pas modifier la structure !!
# il est utilise dans le script networkUpdater.py
manualUpdateHistoryFile = path_SpecificFiles+species+"_manualUpdateHistory.ods"

# the wiki link
# lien vers la page d'accueil du wiki du reseau actuel
# utilise lors de la generation des formulaires de pathways
wikiSite = "http://tisogem.irisa.fr/wiki/index.php/"
# wikiSite = None

# the tgdb from current metacyc version
# Nom du fichier tgdb correspondant a une version donnee de metacyc il
# est utilise dans le script __main__.py, networkUpdater.py et
# wikiGenerator.py.
tgdbRef = path_SpecificFiles+"metacyc_19.0.tgdb"

# metacyc version
# Simple parsing du nom du tgdb afin de recuperer la version.
DBVersion = tgdbRef.split("_")[2].split(".tgdb")[0]

# initial name of the current network
# Nom de la toute premiere version du reseau, ex: Tiso_1.0.tgdbp
# il est utilise dans le script networkUpdater.py
initTgdbpName = str(species)+"_1.0.tgdbp"

# the tgdbp file path of the current network 
#chemin d'acces vers le reseau actuel (du moins le reseau sur lequel on souhaite travailler)
currentTgdbpFile = path_SpecificFiles+"Tiso_1.0.tgdbp"
# current TGDBP version
# Simple parsing du nom du tgdbp afin de recuperer la version.
currentTgdbpVersion = currentTgdbpFile.split("_")[2].split(".tgdbp")[0]

# The default policy in array:
policyInArray = [['class','is a','class'], ['class','has name','name'], ['class','has xref','xref'], ['class','has suppData','suppData'], ['class','is in pathway','pathway'],
        ['compound','is a','class'], ['compound','has name','name'], ['compound','has xref','xref'], ['compound','has suppData','suppData'],
        ['gene','is a','class'], ['gene','has name','name'], ['gene','has xref','xref'], ['gene','has suppData','suppData'], ['gene','codes for','protein'],
        ['pathway','is a','class'], ['pathway','has name','name'], ['pathway','has xref','xref'], ['pathway','is in pathway','pathway'], 
        ['protein','is a','class'], ['protein','has name','name'], ['protein','has xref','xref'], ['protein','has suppData','suppData'], ['protein','catalyses','reaction','assignment','X','score','Y'],
	['protein','is in species','class'], 
	['reaction','is a','class'], ['reaction','has name','name'], ['reaction','has xref','xref'], ['reaction','has suppData','suppData'], ['reaction','is in pathway','pathway'],  
	['reaction','consumes','class'], ['reaction','produces','class'], ['reaction','consumes','compound'], ['reaction','produces','compound'], ['reaction','consumes','protein'],
	['reaction','produces','protein'], ['reaction','is linked to','gene','assignment','X']]

#compartment data:
compartment = {"p":"CCO-PERI-BAC","c":"CCO-CYTOSOL","e":"CCO-EXTRACELLULAR",
	"CCO__45__OUT":"CCO-OUT","CCO__45__IN":"CCO-IN","CCO__45__UNKNOWN__45__SPACE":"CCO-UNKNOWN-SPACE",
	"CCO__45__PM__45__BAC__45__NEG":"CCO-PM-BAC-NEG" ,"CCI__45__PM__45__BAC__45__NEG__45__GN":"CCI-PM-BAC-NEG-GN"}


# Fichier contennant les associations reactions - gene
# et le type d'association (EC-number, ortho...)
assoc_Full = path_SpecificFiles+"assoc_tiso_FULL_metacyc19.0_290715.txt"

# genere avec pantograph, contient les associations reactions - proteins
# et les scores HMM
assoc_HMM = path_SpecificFiles+"assoc_HMM_2907.txt"

# File containing the compartment of reaction
# Fichier 'optionnel' contenant le ou les compartiments ou ont lieu
# les reactions du reseau 
reac_comp = None

# le site de metacyc, utilise dans la creation des pages du wiki
metacycSite = "http://metacyc.org/META/NEW-IMAGE?object="

# Templates de pages wiki:
gene_template = "lib/wikiManager/gene_template.txt"
reaction_template = "lib/wikiManager/reaction_template.txt"
pathway_template = "lib/wikiManager/pathway_template.txt"
metabolite_template = "lib/wikiManager/metabolite_template.txt"


allPathwaysFile = path_Resultats+"allPathways_"+str(species)+str(currentTgdbpVersion)+".tbl"
allMetacycData = path_Resultats+"allMetacycXXData.ods"
