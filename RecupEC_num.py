#!/usr/bin/env python
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from io import StringIO
import copy
from itertools import tee
import bddbis  # execute le truc à l'import
from uniprot import Uniprot

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
# TODO récupérer les num GI, yen a ds le tgdb en tant que "entrez"


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

        # self.detection()

    def detection(self, gbk=None):
        """
        Le gbk master à une partie wgs, que n'a pas le complet. sauf que c'est à la fin du fichier, donc pour opti
        vaut mieux detecter l'absence de cds dans les features.

        :param gbk: Le fichier genbank parsé
        :return: true si c'est le complet, false si master, puis le numéro d'accession primaire , meme si il est déjà dans le fichier..
        """

        comm = gbk.annotations.get("comment", None)  # com est un string, parfois absent dc get
        # /!\/!\/!\ ya une key error, comme par enchantement sur la souche de l'inra
        """
        print(comm[0:18])  # REFSEQ INFORMATION pour tester si ya un primaire
        print(comm[60:68])  # le numero d'accession de l'annot primaire
        """
        access_prim = None
        if comm is not None and comm[0:18] == "REFSEQ INFORMATION":
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

        # les retours:
        list_access_has_refeseq = []
        list_access_has_primaire = []
        list_ec_has_xref = []


        refseq = False
        for motcle in gbk.annotations["keywords"]:
            if motcle == "RefSeq":
                refseq = True

        for donne in gbk.features:  # parcourt les features du fichier gbk(les prots en gros
            if donne.type == "CDS":
                # donne.qualifiers.get("EC_number", "erreurClef: "+str(donne.qualifiers["locus_tag"]))
                num_ec_from_web = donne.qualifiers.get("EC_number", None)  # fait gaffe c'est d listes..
                num_gi_from_web = donne.qualifiers.get("db_xref", None)
                # todo FN806773 UDO:CBL55599.1
                if num_gi_from_web is not None and num_gi_from_web[0][0:3] == "GI:":
                    num_gi_from_web[0] = num_gi_from_web[0][3:]  # modifie pour retirer gi:
                else:
                    num_gi_from_web = None
                # print(num_ec_from_web)
                if num_ec_from_web is not None and num_gi_from_web is not None and refseq:  # pour les gbk refseq
                    # du coup ca ajoute jamais l'accession si ya pas de num ec associé
                    list_access_has_refeseq.append((num_access, num_ec_from_web))  # ajout du tuple
                    list_ec_has_xref.append((num_ec_from_web, num_gi_from_web, num_access))
                    print(num_gi_from_web, ": accessRefseqplacée")

                    # self.inst_rempl.access_has_refeseq(num_access, num_ec_from_web)
                    # self.inst_rempl.ec_has_xref(num_ec_from_web, [next(Uniprot(num_gi_from_web).gener_id())], num_access)

                elif num_ec_from_web is not None and num_gi_from_web is not None:  # pour les gbk non refseq
                    list_access_has_primaire.append((num_access, num_ec_from_web))
                    list_ec_has_xref.append((num_ec_from_web, num_gi_from_web, num_access))
                    print(num_gi_from_web, ": primairePlacée")

                    # self.inst_rempl.access_has_primaire(num_access, num_ec_from_web)
                    # self.inst_rempl.ec_has_xref(num_ec_from_web, [next(Uniprot(num_gi_from_web).gener_id())], num_access)  # pb qd géné vide, ok
                    # # TODO faire gaffe ya plusieurs accession uniprot associées parfois.. bon ca prend la première qui est pas mal généralement

        return list_access_has_refeseq, list_access_has_primaire, list_ec_has_xref

    def insertion_bdd(self, datarefseq):
        list_access_has_refeseq = datarefseq[0]
        list_access_has_primaire = datarefseq[1]
        list_ec_has_xref = datarefseq[2]

        if len(list_access_has_refeseq) != 0:  # si c'est un refseq, la liste n'est pas vide
            for prot in list_access_has_refeseq:
                self.inst_rempl.access_has_refeseq(prot[0], prot[1])  # le tuple des bonnes donnée..
                print("ajoutRefseq_insertion_bdd")

        else:
            for prot_pri in list_access_has_primaire:
                self.inst_rempl.access_has_primaire(prot_pri[0], prot_pri[1])
                print("ajoutPrimaire_insertion_bdd")


        # /!\/!\/!\ hashtag degeulasse
        vielle_ref = []
        for ref in list_ec_has_xref:
            vielle_ref.append(ref[1][0])  # car ref est une liste de 1 element..

        nvl_ref = Uniprot(vielle_ref).gener_id()  # /!\/!\/!\ c un générateur..

        for i in range(0, len(list_ec_has_xref)):
            self.inst_rempl.ec_has_xref(list_ec_has_xref[i][0], [next(nvl_ref)], list_ec_has_xref[i][2])
            print("ajoutXrefUniprot_insertion_bdd")


    ##################################################################
    "Partie recup des accessions à partir d'un master record (NZ_AZSI00000000)"
    ##################################################################

    def recup_master_access(self, gbk=None):
        """
        Génère à partir d'un gbk master record, les identifiants vers les sous gbk.
        """
        rangeaccess = gbk.annotations["wgs"]  # ou wgs scaffold? il ont l'air de plus faire dériver vers des refseq

        def gener_access(paramrangeaccess):
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
    recu = Recup_EC()  # instance de la classe entière
    """
    NZ_AZSI00000000 (master)
    NZ_CP009472.1
    """
    print("Pense à supprimer la bdd si tu veux ecraser les données..")

    def traitement(access):  # appelé une fois par bactérie
        gbk = recu.telecharge(access)  # le fichier gbk de la bacterie que l'on telecharge
        test_parse = gbk  # ce sont des fichiers virtuels, dc nrmlt plus de generateurs...
        gbk_gener = gbk
        # tt ce bordel etait à cause du générateur, nrmlt c fini

        detection = recu.detection(test_parse)  # [0] bool, true si complet. [1] num_acc

        if detection[0]:  # faut que testparse renvoi aussi le type d'annotations(?) Cas des gbk complets, pas wgs
            print("complet")
            print(access)  # c'est bien un str
            data_refseq = recu.recup_ec(gbk_gener, access)  # pour télécharger la version refseq
            recu.insertion_bdd(data_refseq)
            if detection[1] is not None:  # ca veut dire qu'il y a un numéro d'acc primaire
                gbk_prot = recu.telecharge(detection[1])  # telécharge la version annot primaire
                data_prim = recu.recup_ec(gbk_prot, access)  # je laisse le num ec refseq
                recu.insertion_bdd(data_prim)

        else:  # cas des master record
            print("master")
            for accessBis in recu.recup_master_access(gbk_gener):  # genere les identifiants vers les gbk du master
                gbkprot = recu.telecharge(accessBis)
                data_master = recu.recup_ec(gbkprot, access)  # bon le script marche, mais les nums ec n'y sont pas présents, sauf dans les notes
                recu.insertion_bdd(data_master)
                print("insert_master")

        # gbk.close()  # pas oublier de le fermer.. bah de toutes facon c'est la merde, ca fuit de partout


    with open('exemple/ListeAccess', mode='r') as listaccess:
        for numacc in listaccess:  # itère la liste des accessions à regarder
            traitement(numacc.strip())  # gaffe aux espaces à la fin du doc.. le strip pour enlever les \n...


# instantiation des classes de bbdbis pr test
"""
inst_req = bddbis.Requetes()
inst_req.print_table_access()

inst_remp = bddbis.Remplissage()
"""