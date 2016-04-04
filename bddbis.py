#!/usr/bin/env python
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
"""
incrementation auto des ids, pas d'unicité par contre... pour les accessions
ou alors mettre son identifiant en clé..
"""

eng = create_engine('sqlite:///testBis.balec')

Base = declarative_base()

# Tables d'association:
association_table_refeseq = Table('association', Base.metadata,  # renomer association+tard (mais déplace l'acces mem
    Column('Accessions_tab_id', String, ForeignKey('Accessions_tab.Id_access')),
    Column('EC_numbers_tab_id', String, ForeignKey('EC_numbers_tab.Id_ec'))
)
association_table_primaire = Table('association_primaire', Base.metadata,
    Column('Accessions_tab_id', String, ForeignKey('Accessions_tab.Id_access')),
    Column('EC_numbers_tab_id', String, ForeignKey('EC_numbers_tab.Id_ec'))
)
association_table_xref = Table('association_xref', Base.metadata,
    Column('Xref_tab_id', String, ForeignKey('Xref_tab.Id_xref')),
    Column('EC_numbers_tab_id', String, ForeignKey('EC_numbers_tab.Id_ec'))
)
association_table_xref_acc = Table('association_xref_acc', Base.metadata,
    Column('Accessions_tab_id', String, ForeignKey('Accessions_tab.Id_access')),
    Column('Xref_tab_id', String, ForeignKey('Xref_tab.Id_xref'))
)


####################################################################
"Objets de la BDD"
####################################################################


class Accessions(Base):  # le truc (Base) c'est l'héritage

    __tablename__ = "Accessions_tab"
    # __tableargs__h soit index soit contrainte unicité.

    # Id = Column(Integer, primary_key=True, autoincrement=True)  # auto increment va gérer les id tt seul
    Id_access = Column(String, primary_key=True)

    #Les relations
    hasRefSeq = relationship("EC_numbers", secondary=association_table_refeseq, back_populates="hasAccesByRefSeq")
    hasPrimaire = relationship("EC_numbers", secondary=association_table_primaire, back_populates="hasAccesByPrimaire")
    uniHasAccess = relationship("Xref", secondary=association_table_xref_acc, back_populates="xrefHasAccess")
    # le nom est nul, ce serait plutot accessHasUni

class EC_numbers(Base):  # mettre en camelCase

    __tablename__ = "EC_numbers_tab"

    Id_ec = Column(String, primary_key=True)

    hasAccesByRefSeq = relationship("Accessions", secondary=association_table_refeseq, back_populates="hasRefSeq")
    hasAccesByPrimaire = relationship("Accessions", secondary=association_table_primaire, back_populates="hasPrimaire")
    hasXref = relationship("Xref", secondary=association_table_xref, back_populates="hasEc")

class Xref(Base):

    __tablename__ = "Xref_tab"

    Id_xref = Column(String, primary_key=True)

    hasEc = relationship("EC_numbers", secondary=association_table_xref, back_populates="hasXref")
    xrefHasAccess = relationship("Accessions", secondary=association_table_xref_acc, back_populates="uniHasAccess")
    # on met hasprimaire, mais en fait vaut mieux recreer un autre truc

# Ne pas mettre au dessus...
Base.metadata.bind = eng
Base.metadata.create_all()

Session = sessionmaker(bind=eng)
ses = Session()
####################################################################
"Remplissages des tables"
####################################################################


class Remplissage:

    def __init__(self):
        pass

    @staticmethod
    def ajout_access(param_access):  # gérer les doublons: plutot utiliser first car ne renvoit pas d''exeptions mais None
        if ses.query(Accessions).filter(Accessions.Id_access == param_access).first() is None:
            ses.add(Accessions(Id_access=param_access))
            ses.commit()

    @staticmethod
    def ajout_ec(param_num_ec):  # bon théoriquement ca devrait jamais arriver si c'est bien fait
        if ses.query(EC_numbers).filter(EC_numbers.Id_ec == param_num_ec).first() is None:
            ses.add(EC_numbers(Id_ec=param_num_ec))
            ses.commit()

    @staticmethod
    def ajout_xref(param_xref):
        if ses.query(Xref).filter(Xref.Id_xref == param_xref).first() is None:
            ses.add(Xref(Id_xref=param_xref))
            ses.commit()

    def access_has_refeseq(self, param_id_access, param_list_ec):  #faudra test les exeptions aussi qd mm  §§§§CORRIGER LE TYPO!!!!
        """

        :param param_id_access:
        :param param_list_ec: c'est quand on change les numéros de la liste que ca bug, ca les ajoute mais trop tard..
        :return:
        """
        list_objet_ec = []
        for ec in param_list_ec:  # parcourt la liste des strings du param, par contre parcourt les lettres si juste srt
            Remplissage.ajout_ec(ec)  #guette si le truc est déjà la ou non
            selec_ec = ses.query(EC_numbers).filter(EC_numbers.Id_ec == ec).first()
            list_objet_ec.append(selec_ec)

        Remplissage.ajout_access(param_id_access)  #test et ajoute si c pas déjà là
        selec = ses.query(Accessions).filter(Accessions.Id_access == param_id_access).first()  # pour l'accession

        selec.hasRefSeq += list_objet_ec
        ses.add(selec)
        ses.flush()  #pas forcement utile..
        ses.commit()

    def access_has_primaire(self, param_id_access, param_list_ec):
        """

        :param param_id_access:
        :param param_list_ec:
        :return:
        """
        list_objet_ec = []
        for ec in param_list_ec:  # parcourt la liste des strings du param, par contre parcourt les lettres si juste srt
            Remplissage.ajout_ec(ec)  # guette si le truc est déjà la ou non
            selec_ec = ses.query(EC_numbers).filter(EC_numbers.Id_ec == ec).first()
            list_objet_ec.append(selec_ec)

        Remplissage.ajout_access(param_id_access)  #test et ajoute si c pas déjà là
        selec = ses.query(Accessions).filter(Accessions.Id_access == param_id_access).first()  # pour l'accession

        selec.hasPrimaire += list_objet_ec  # la seule ligne qui change entre les fct
        ses.add(selec)
        ses.commit()

    # todo ajouter l'accession (replace.replace, str.maketrans...
    def ec_has_xref(self, param_list_ec, param_list_xref, param_access):  # etre bien sur que c'est toujours des gi..
        list_objet_ec = []
        for ec in param_list_ec:  # parcourt la liste des strings du param, par contre parcourt les lettres si juste srt
            Remplissage.ajout_ec(ec)  # guette si le truc est déjà la ou non
            selec_ec = ses.query(EC_numbers).filter(EC_numbers.Id_ec == ec).first()
            list_objet_ec.append(selec_ec)

        Remplissage.ajout_xref(param_list_xref[0])  # on prend le premier en espérant qu'il n'y a q'une cross ref par ec
        selec = ses.query(Xref).filter(Xref.Id_xref == param_list_xref[0]).first()
        selec.hasEc += list_objet_ec
        # l'accession doit bien être présente à la base, nrmlt c'est bon
        selec.xrefHasAccess += [ses.query(Accessions).filter(Accessions.Id_access == param_access).first()]
        ses.add(selec)
        ses.commit()

####################################################################
"Test de remplissage"
####################################################################

listAccessTruc = ["stringEC3", "stringEC4"]

# inst_remplissage = Remplissage()
# inst_remplissage.ajout_access("grande bzacterie1")
# inst_remplissage.ajout_ec("mechantNum2")
# inst_remplissage.access_has_refeseq("grande bzacterie", listAccessTruc)
#
# inst_remplissage.access_has_refeseq("acc1", ["2"])
# inst_remplissage.access_has_primaire("acc2", ["3"])
###################################################################
"Requete sur les Tables et les relations "
####################################################################


class Requetes:

    def __init__(self):
        pass

    @staticmethod
    def print_table_access():
        resulAcc = ses.query(Accessions).all()
        for laccessin in resulAcc:
            print("ID de l'accession: ", laccessin.Id_access, sep=" ")
            for obj in laccessin.hasRefSeq:
                print(" Id du num EC de RefSeq:", obj.Id_ec, "/", end="", sep=" ")
            print("\n")
            for obj in laccessin.hasPrimaire:
                print(" Id du num EC de Primaire:", obj.Id_ec, "/", end="", sep=" ")
            print("\n")
            pass

    @staticmethod
    def print_table_ecnum():
        resulEc = ses.query(EC_numbers).all()
        for laccessinBis in resulEc:
            print("ID du num EC: ", laccessinBis.Id_ec, sep=" ")
            listobjet = set(laccessinBis.hasAccesByRefSeq + laccessinBis.hasAccesByPrimaire)
            # ben ya plus qu'a les rendre unique...
            for obj in listobjet:
                print(" Id de l'access: ", obj.Id_access, "/", end="", sep=" ")
            print("\n")
            listref = laccessinBis.hasXref
            for obj in listref:
                print(" Id de la ref: ", obj.Id_xref, "/", end="", sep=" ")
            print("\n")


    @staticmethod
    def print_table_xref():
        resul_xref = ses.query(Xref).all()
        for xref in resul_xref:
            print("Id de la ref: ", xref.Id_xref, sep=" ")
            listobj = xref.hasEc
            for obj in listobj:
                print("Id de l'ec: ", obj.Id_ec, "/", end="", sep=" ")
            print("\n")

    @staticmethod
    def print_rdf():
        resul_ec = ses.query(EC_numbers).all()
        for num in resul_ec:
            accessions_refseq = num.hasAccesByRefSeq  # TODO enlever les "" pour les id access, et pr les ec ds le rdf
            for acc in accessions_refseq:
                yield "metagdb:"+num.Id_ec+" metagdb:hasannot_refseq metagdb:"+acc.Id_access
            accessions_primaire = num.hasAccesByPrimaire
            for acc in accessions_primaire:
                yield "metagdb:"+num.Id_ec+" metagdb:hasannot_primaire metagdb:"+acc.Id_access
                # TODO je sais plus si ca marche a force..

    @staticmethod
    def write_asp():
        with open("ASP/test_asp.lp", "w") as asp_file:
            resul_ec = ses.query(EC_numbers).all()
            for num in resul_ec:  # num correspond au numero ec
                list_xref = num.hasXref  # la liste des xref du num_ec

                list_access_refseq = num.hasAccesByRefSeq  # liste de ses acc NCBI
                list_access_primaire = num.hasAccesByPrimaire
                for xref in list_xref:  # défile les xref d'un EC
                    yield "uniprot( ec("+num.Id_ec.replace(".", ',').replace(",-", "")+"),\""+xref.Id_xref+"\")."
                    for acc in list_access_refseq:  # défile les acc d'un ec, ecrit en fct de l'xref, type inférence
                        yield "num_access(\""+acc.Id_access+"\",\""+xref.Id_xref+"\", \"REFSEQ\")."

                    for acc in list_access_primaire:
                        yield "num_access(\""+acc.Id_access+"\",\""+xref.Id_xref+"\", \"PRIMAIRE\")."

    @staticmethod
    def statistiques_par_access():
        resulAcc = ses.query(Accessions).all()
        total_ec_refseq = 0
        total_ec_primaire = 0
        for i, acc in enumerate(resulAcc):
            list_ec_refseq = acc.hasRefSeq
            for j, ec in enumerate(list_ec_refseq):
                pass
            print("nb d'ec refseq de l'access: ", j)
            total_ec_refseq += j

            list_ec_primaire = acc.hasPrimaire
            try:
                for numP, ecc in enumerate(list_ec_primaire): #faire un try execpt, ou un if pour les nones
                    pass
                print("nb d'ec primaire de l'access: ", numP)
                total_ec_primaire += numP
            except:
                print("ya un ti bug dans les stats")
            pass

        print("Nombre de access: ", i)
        print("Nombre de ec refseq: ", total_ec_refseq)
        print("Nombre de ec primaire: ", total_ec_primaire)

    @staticmethod
    def print_has_refseq(self, param_accession):
        resuRela = ses.query()  # boh en fait c'est a moitié déjà fait

    # print(association_table.c.Accessions_tab_id)

requetes = Requetes()  # instance de la classe requetes
# requetes.statistiques_par_access()
# requetes.print_table_access()
# requetes.print_table_ecnum()
# requetes.print_table_xref()
# for i in requetes.print_rdf():
#     print(i)


""
with open('ASP/ec_uni.lp', 'w') as fich_asp:
    for i in requetes.write_asp():
        print(i)
        fich_asp.write(i+"\n")
""

