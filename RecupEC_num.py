#!/usr/bin/env python
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from BaseDeDonnees import BaseDDCl
import copy
from itertools import tee

"""
Installation des modules(en -user si pas root):
"""
"""
Questions:
- comment appeler des méthodes dans d'autres méthodes? (sans refaire d'instances..)
- comment créer une persistance des données en dehors du statement with?
- try exepect stop iteration pour le generateur
"""
class Recup_EC :
    ##################################################################
    "Partie recuperation"
    ##################################################################

    def __init__(self):
        """

        :return:
        """
        Entrez.email = "ouiouioui@wanadoo.fr"

    def telecharge(self, accession):

        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gbwithparts", retmode="txt")

        gbk = handle.read()

        #self.detection()

        """
        with open("exemple/gbwithparts_Refseq_Master", 'w') as fichier:  # ok ca marche faut juste créer la directory
            fichier.write(textt)
        """

    def detection(self, gbk=None):
        """
        Le gbk master à une partie wgs, que n'a pas le complet. sauf que c'est à la fin du fichier, donc pour opti
        vaut mieux detecter l'absence de cds dans les features.

        :param gbk: Le fichier genbank parsé
        :return: true si c'est le complet, false si master
        """

        for donne in gbk:
            # print(donne.annotations)  # d'ou vient ce bout de sequence??
            if "wgs" in donne.annotations:
                return False

        return True



    ######################################################################
    "Partie recup numeroEC à partir d'un genbank complet (NZ_CP009472.1)"
    ######################################################################

    def recup_ec(self, gbk):
        """

        :param gbk: Le fichier genbank dejà parsé
        :return:
        """

        for donne in next(gbk).features:  # bug ici...
            if donne.type == "CDS":
                print(donne.qualifiers.get("EC_number", "erreurClef: "+str(donne.qualifiers["locus_tag"])))
                # le get fait une sorte d'exeption


    ##################################################################
    "Partie recup des accessions à partir d'un master record (NZ_AZSI00000000)"
    ##################################################################

    def recup_master_access(self, gbk=None):
        """
        """
        for donne in gbk:  # pb de gbk vide, car déjà epuisé.
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

        return gener_access(rangeaccess)



    ##################################################################
    "Partie SQLalchemy"
    ##################################################################

if __name__ == "__main__":
    recu = Recup_EC()
    with open("exemple/gbwithparts_Refseq_Complet", 'r') as fichierGBKcomplet:
        fichierParseComplet = SeqIO.parse(fichierGBKcomplet, 'genbank')
        #recu.recup_ec(fichierParseComplet)

    with open("exemple/gbwithparts_Refseq_Master", 'r') as fichierGBKmaster:
        fichierParseMaster = SeqIO.parse(fichierGBKmaster, 'genbank')
        #recu.recup_master_access(fichierParseMaster)

    #gbwithparts_Refseq_Master
    #gbwithparts_Refseq_Complet
    with open("exemple/gbwithparts_Refseq_Master", 'r') as test:
        test_parse, gbk_gener = tee( SeqIO.parse(test, 'genbank') ) # ok, tee de itertools permet de creer plusieur gener
        #gbk_gener = SeqIO.parse(test, 'genbank')
        # print(recu.detection(test_parse))
        if recu.detection(test_parse) == True:
            print("complet")  # c'est faux...
            recu.recup_ec(gbk_gener)  # ici itérer avec le second generateur cree par tee

        else :
            print("master")
            recu.recup_master_access(gbk_gener)  # faire une boucle de telechargement ici
            # puis pour chaque telechargement un recu.recup_ec()

"""
    bdd = BaseDDCl()
    bdd.test()
    bdd.construction()
"""