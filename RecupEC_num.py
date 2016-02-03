#!/usr/bin/env python
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from io import StringIO
import copy
from itertools import tee
import bddbis  # execute le truc à l'import

"""
Installation des modules(en -user si pas root):
"""
"""
Questions:
- comment appeler des méthodes dans d'autres méthodes? (sans refaire d'instances..) self.methode crétin
- comment créer une persistance des données en dehors du statement with?
- try exepect stop iteration pour le generateur

Révélations: le générateur est composé d'un record, donc renovyer juste un next serait pas mal
"""
class Recup_EC :
    ##################################################################
    "Partie recuperation"
    ##################################################################

    def __init__(self):
        """

        :return:
        """
        Entrez.email = "ouiou@wanadoo.fr"  # necessaire pour se connecte à Entrez..

        self.inst_rempl = bddbis.Remplissage()

    def telecharge(self, accession):

        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gbwithparts", retmode="txt")

        gbk_handle = handle.read()
        gbkIO = StringIO(gbk_handle)  # sauvegarde dans un fichier virtuel
        handle.close()
        gbk = SeqIO.parse(gbkIO, 'genbank')  # essayer de faire un next pour prendre
        # fermer gbkIO? ben on peut pas sinon c op sur closed file..
        return next(gbk)

        #self.detection()

    def detection(self, gbk=None):
        """
        Le gbk master à une partie wgs, que n'a pas le complet. sauf que c'est à la fin du fichier, donc pour opti
        vaut mieux detecter l'absence de cds dans les features.

        :param gbk: Le fichier genbank parsé
        :return: true si c'est le complet, false si master, puis le numéro d'accession , meme si il est déjà dans le fichier..
        """

        comm = gbk.annotations["comment"]  # com est un string
        # /!\/!\/!\ ya une key error, comme par enchantement sur la souche de l'inra
        """
        print(comm[0:18])  # REFSEQ INFORMATION pour tester si ya un primaire
        print(comm[60:68])  # le numero d'accession de l'annot primaire
        """
        access_prim = None
        if comm[0:18] == "REFSEQ INFORMATION":
            access_prim = comm[60:68]

        for cle in gbk.annotations:  # permet de tester si le fichier est un master record
            if cle == "wgs":
                return False, access_prim

        return True, access_prim



    ######################################################################
    "Partie recup numeroEC à partir d'un genbank complet (NZ_CP009472.1)"
    ######################################################################

    def recup_ec(self, gbk, num_access):
        """
        Cette fonction insert les numero ec dans la base de donnée, associés à la bonne accession fournie en param
        /!\ Faut aussi préciser le type d'annotation.. Regarder dans "keywords", et l'annotation originale se trouve
        dans "comment"
        :param gbk: Le fichier genbank dejà parsé
        :param num_access: le numero d'accession, qui vient de la liste d'accessions fournie
        :return:
        """

        refseq = False
        for motcle in gbk.annotations["keywords"]:
            if motcle == "RefSeq":
                refseq = True

        for donne in gbk.features:
            if donne.type == "CDS":
                # donne.qualifiers.get("EC_number", "erreurClef: "+str(donne.qualifiers["locus_tag"]))
                num_ec_from_web = donne.qualifiers.get("EC_number", None)  # bon ca doit etre une liste jimagine vu que ca marche
                # print(num_ec_from_web)
                if num_ec_from_web is not None and refseq:  # du coup ca ajoute jamais l'accession si ya pas de num ec associé
                    self.inst_rempl.access_has_refeseq(num_access, num_ec_from_web)
                    # print("accesplacée")
                elif num_ec_from_web is not None:
                    self.inst_rempl.access_has_primaire(num_access, num_ec_from_web)
                    # print("primairePlacée")

    ##################################################################
    "Partie recup des accessions à partir d'un master record (NZ_AZSI00000000)"
    ##################################################################

    def recup_master_access(self, gbk=None):
        """
        """
        rangeaccess = gbk.annotations["wgs"]  # ou wgs scaffold? il ont l'air de plus faire dériver vers des refseq

        def gener_access(paramrangeaccess):  # essayer de faire un foutu générateur...
            start = paramrangeaccess[0]
            stop = paramrangeaccess[1]
            locus = start[0:5]  # on rajoute le 0 qui se trouve devant le 1
            nombre_sta = int(start[5:12])  # on garde le 1 du début pour que ca affiche les 0 tout en étant un int
            nombre_sto = int(stop[5:12])
            print(stop)
            print(locus)
            print(nombre_sta)
            print(nombre_sto)

            for nombre in range(nombre_sta, nombre_sto + 1, 1):
                sortie = locus + str(nombre)
                # print(locus + str(nombre))
                yield sortie

        return gener_access(rangeaccess)

    ##################################################################
    "Partie SQLalchemy"
    ##################################################################

if __name__ == "__main__":
    recu = Recup_EC()
    """
    NZ_AZSI00000000 (master)
    NZ_CP009472.1
    """
    def traitement(access):
        gbk = recu.telecharge(access)

        # test_parse, gbk_gener = tee(gbk)  # ok, tee de itertools permet de creer plusieur generateurs
        test_parse = gbk
        gbk_gener = gbk

        detection = recu.detection(test_parse)

        if detection[0]:  # faut que testparse renvoi aussi le type d'annotations
            print("complet")
            print(access)  # c'est bien un str
            recu.recup_ec(gbk_gener, access)
            if detection[1] is not None:
                gbk_prot = recu.telecharge(detection[1])
                recu.recup_ec(gbk_prot, access)  # je laisse le num ec refseq

        else:
            print("master")
            for accessBis in recu.recup_master_access(gbk_gener):  # faire une boucle de telechargement ici
                gbkprot = recu.telecharge(accessBis)
                recu.recup_ec(gbkprot, access)  # bon le script marche, mais les nums ec n'y sont pas présents, sauf dans les notes

        # gbk.close()  # pas oublier de le fermer.. bah de toutes facon c'est la merde, ca fuit de partout


    with open('exemple/ListeAccess', mode='r') as listaccess:
        for numacc in listaccess:  # itère la liste des accessions à regarder
            # print("le num d'acc qui ne s'affiche aps", numacc)
            traitement(numacc)  # gaffe aux espaces à la fin du doc..


# instantiation des classes de bbdbis pr test
"""
inst_req = bddbis.Requetes()
inst_req.print_table_access()

inst_remp = bddbis.Remplissage()
"""