#!/usr/bin/env python
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
"""
incrementation auto des ids, pas d'unicité par contre... pour les accessions
ou alors mettre son identifiant en clé..
trouver un moyen de mettre à jour les relations..
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

####################################################################
"Objets de la BDD"
####################################################################


class Accessions(Base):  # le truc (Base) c'est l'héritage

    __tablename__ = "Accessions_tab"

    # Id = Column(Integer, primary_key=True, autoincrement=True)  # auto increment va gérer les id tt seul
    Id_access = Column(String, primary_key=True)

    #Les relations
    hasRefSeq = relationship("EC_numbers", secondary=association_table_refeseq, back_populates="hasAccesByRefSeq")
    hasPrimaire = relationship("EC_numbers", secondary=association_table_primaire, back_populates="hasAccesByPrimaire")


class EC_numbers(Base):  # mettre en camelCase

    __tablename__ = "EC_numbers_tab"

    Id_ec = Column(String, primary_key=True)
    hasAccesByRefSeq = relationship("Accessions", secondary=association_table_refeseq, back_populates="hasRefSeq") # mouais, mais hasprimaire alors?
    hasAccesByPrimaire = relationship("Accessions", secondary=association_table_primaire, back_populates="hasPrimaire")

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
    def ajout_access(param_access): #gérer les doublons: plutot utiliser first car ne renvoit pas d''exeptions mais None
        if ses.query(Accessions).filter(Accessions.Id_access == param_access).first() is None:
            ses.add(Accessions(Id_access=param_access))
            ses.commit()

    @staticmethod
    def ajout_ec(param_num_ec): # bon théoriquement ca devrait jamais arriver si c'est bien fait
        if ses.query(EC_numbers).filter(EC_numbers.Id_ec == param_num_ec).first() is None:
            ses.add(EC_numbers(Id_ec=param_num_ec))
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
            Remplissage.ajout_ec(ec)  #guette si le truc est déjà la ou non
            selec_ec = ses.query(EC_numbers).filter(EC_numbers.Id_ec == ec).first()
            list_objet_ec.append(selec_ec)

        Remplissage.ajout_access(param_id_access)  #test et ajoute si c pas déjà là
        selec = ses.query(Accessions).filter(Accessions.Id_access == param_id_access).first()  # pour l'accession

        selec.hasPrimaire += list_objet_ec  # la seule ligne qui change entre les fct
        ses.add(selec)
        ses.commit()


####################################################################
"Test de remplissage"
####################################################################

listAccessTruc = ["stringEC3", "stringEC4"]

inst_remplissage = Remplissage()
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
                print(" Id de l'access: ", obj.Id_access, "/", end="")
            print("\n")
            pass

    @staticmethod
    def print_has_refseq(self, param_accession):
        resuRela = ses.query()  # boh en fait c'est a moitié déjà fait

    # print(association_table.c.Accessions_tab_id)

requetes = Requetes()  # instance de la classe requetes
requetes.print_table_access()
requetes.print_table_ecnum()



