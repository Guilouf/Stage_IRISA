#!/usr/bin/env python
from Bio import Entrez, SeqIO
from io import StringIO
from Bio.SeqRecord import SeqRecord
from BaseDeDonnees import BaseDDCl
import copy
from itertools import tee

"""
Installation des modules(en -user si pas root):
"""
"""
Questions:
- comment appeler des méthodes dans d'autres méthodes? (sans refaire d'instances..) self.methode crétin
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
        """
        bon apparement le read serait pour le xml..
        :param accession:
        :return:
        """
        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gbwithparts", retmode="txt")

        gbk =  handle.read() #readline marche aussi, mais renvoit juste une ligne
        gbk = StringIO(gbk)
        #print(gbk.read()) # bon ca marche parfaitement bien, sauf si on fait le read en dehors de la fct..
        #GenBankScanner.parse(handle)
        handle.close()
        return gbk   # je l'ai passé en handle tout court


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
                sortie = locus + str(nombre)
                print(locus + str(nombre))
                yield sortie

        return gener_access(rangeaccess)



    ##################################################################
    "Partie SQLalchemy"
    ##################################################################

if __name__ == "__main__":
    recu = Recup_EC()
    """
    with open("exemple/gbwithparts_Refseq_Complet", 'r') as fichierGBKcomplet:
        fichierParseComplet = SeqIO.parse(fichierGBKcomplet, 'genbank')
        #recu.recup_ec(fichierParseComplet)
    """
    #test à partir du handle..
    handleRead = recu.telecharge("NZ_AZSI00000000")
    fichierParseMaster = SeqIO.parse(handleRead, 'genbank')
    #print(handleRead.read())
    print("putain que ca m'enerve..")

    putainhandle = handleRead
    print(putainhandle)
    #print(fichierParseMaster)

    for i in putainhandle: # le generateur bug avec le handle...
        print(i)


    for machin in SeqIO.parse(handleRead, 'genbank'):
        print(machin)




    with open("exemple/gbwithparts_Refseq_Master", 'r') as fichierGBKmaster:
        fichierParseMaster = SeqIO.parse(fichierGBKmaster, 'genbank')
        #fichierParseMaster = recu.telecharge("NZ_AZSI00000000")
        #fichierParseMaster = SeqIO.parse(recu.telecharge("NZ_AZSI00000000"), 'genbank')
        #recu.recup_master_access(fichierParseMaster)

    #gbwithparts_Refseq_Master
    #gbwithparts_Refseq_Complet
    """
    with open("exemple/gbwithparts_Refseq_Master", 'r') as test:
        test_parse, gbk_gener = tee( SeqIO.parse(test, 'genbank') ) # ok, tee de itertools permet de creer plusieur gener
        #gbk_gener = SeqIO.parse(test, 'genbank')
        # print(recu.detection(test_parse))
        if recu.detection(test_parse) == True:
            print("complet")  # c'est faux...
            recu.recup_ec(gbk_gener)  # ici itérer avec le second generateur cree par tee

        else:
            print("master")
            for access in recu.recup_master_access(gbk_gener):  # faire une boucle de telechargement ici
                pass # mm en pass ca active le generateur
            # puis pour chaque telechargement un recu.recup_ec()
    """
"""
    bdd = BaseDDCl()
    bdd.test()
    bdd.construction()
"""