#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord

"""
partie recuperation
"""

Entrez.email = "ouiouioui@wanadoo.fr"

handle = Entrez.efetch(db="nucleotide", id="NZ_CP009472.1" ,rettype="gbwithparts", retmode="txt")

textt = handle.read()


fichier = open("FichierRecup", 'w')

fichier.write(textt)


"""
partie traitement
"""

fichier = open("GenBankNuclParts", 'r')
fichierParse = SeqIO.parse(fichier, 'genbank')

for donne in next(fichierParse).features:
  if (donne.type == "CDS"):
    print(donne.qualifiers.get("EC_number", "erreurClef"+str(donne.qualifiers["locus_tag"])))	#mettre une exeption, parfois le champ n'existe pas..

