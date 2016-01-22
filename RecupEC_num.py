#!/usr/bin/env python
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord

"""
Installation des modules(en -user si pas root):
"""

"""############
Partie recuperation
############"""

"""
Entrez.email = "ouiouioui@wanadoo.fr"

handle = Entrez.efetch(db="nucleotide", id="NZ_AZSI00000000" ,rettype="gbwithparts", retmode="txt")

textt = handle.read()


fichier = open("exemple/gbwithparts_Refseq_Master", 'w')  # ok ca marche faut juste créer la directory

fichier.write(textt)
"""

"""###########
Partie recup numeroEC à partir d'un genbank complet (NZ_CP009472.1)
###########"""

"""
fichierGBKcomplet = open("exemple/gbwithparts_refseqComplet", 'r')
fichierParseComplet = SeqIO.parse(fichierGBKcomplet, 'genbank')

for donne in next(fichierParseComplet).features:
    if donne.type == "CDS":
        print(donne.qualifiers.get("EC_number", "erreurClef"+str(donne.qualifiers["locus_tag"])))  # mettre une exeption, parfois le champ n'existe pas..
"""

"""##########
Partie recup des accessions à partir d'un master record (NZ_AZSI00000000)
##########"""

with open("exemple/gbwithparts_Refseq_Master", 'r') as fichierMaster:
    fichierParseMaster = SeqIO.parse(fichierMaster, 'genbank')  # bug là dedans...

    for donne in fichierParseMaster:
        rangeaccess = donne.annotations["wgs"]

def generAccess(rangeaccess):  # essayer de faire un foutu générateur...
    start = rangeaccess[0]
    stop = rangeaccess[1]
    print(stop)
    locus = start[0:5]  # on rajoute le 0 qui se trouve devant le 1
    nombreSta = int(start[5:12])  # on garde le 1 du début pour que ca affiche les 0 tout en étant un int
    nombreSto = int(stop[5:12])
    print(locus)
    print(nombreSta)
    print(nombreSto)

    for nombre in range(nombreSta, nombreSto + 1, 1):
        print(locus + str(nombre))

generAccess(rangeaccess)
