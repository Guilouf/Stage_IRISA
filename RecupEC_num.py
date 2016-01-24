#!/usr/bin/env python
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from BaseDeDonnees import BaseDDCl
import copy

"""
Installation des modules(en -user si pas root):
"""
class Recup_EC :
    ##################################################################
    "Partie recuperation"
    ##################################################################

    def __init__(self):
        Entrez.email = "ouiouioui@wanadoo.fr"



    def telecharge(self, accession):

        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gbwithparts", retmode="txt")

        gbk = handle.read()

        """
        with open("exemple/gbwithparts_Refseq_Master", 'w') as fichier:  # ok ca marche faut juste créer la directory
            fichier.write(textt)
        """

    ######################################################################
    "Partie recup numeroEC à partir d'un genbank complet (NZ_CP009472.1)"
    ######################################################################

    def recup_ec(self):

        with open("exemple/gbwithparts_refseqComplet", 'r') as fichierGBKcomplet:  # il est automatiquement fermé..
            fichierParseComplet = SeqIO.parse(fichierGBKcomplet, 'genbank')  # comment affecter par copie?

        for donne in next(fichierParseComplet).features:  # bug ici...
            if donne.type == "CDS":
                print(donne.qualifiers.get("EC_number", "erreurClef"+str(donne.qualifiers["locus_tag"])))
                # le get fait une sorte d'exeption


    ##################################################################
    "Partie recup des accessions à partir d'un master record (NZ_AZSI00000000)"
    ##################################################################

    def recup_master_access(self):
        """
        with open("exemple/gbwithparts_Refseq_Master", 'r') as fichierMaster:
            fichierParseMaster = copy.copy(SeqIO.parse(fichierMaster, 'genbank'))
        """
        fichierMaster = open("exemple/gbwithparts_Refseq_Master", 'r')
        fichierParseMaster = SeqIO.parse(fichierMaster, 'genbank')
        for donne in fichierParseMaster:
            # help(donne)
            rangeaccess = donne.annotations["wgs"]


        def gener_access(paramrangeaccess):  # essayer de faire un foutu générateur...
            start = paramrangeaccess[0]
            stop = paramrangeaccess[1]
            print(stop)
            locus = start[0:5]  # on rajoute le 0 qui se trouve devant le 1
            nombre_sta = int(start[5:12])  # on garde le 1 du début pour que ca affiche les 0 tout en étant un int
            nombre_sto = int(stop[5:12])
            print(locus)
            print(nombre_sta)
            print(nombre_sto)

            for nombre in range(nombre_sta, nombre_sto + 1, 1):
                print(locus + str(nombre))


        gener_access(rangeaccess)

    ##################################################################
    "Partie SQLalchemy"
    ##################################################################
if __name__ == "__main__":
    Recup_EC()
    Recup_EC().recup_master_access()
    BaseDDCl()
    BaseDDCl().test()
    BaseDDCl().construction()
