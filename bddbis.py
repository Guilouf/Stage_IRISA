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

# Table d'association
association_table = Table('association', Base.metadata,
    Column('Accessions_tab_id', String, ForeignKey('Accessions_tab.Id_access')),
    Column('EC_numbers_tab_id', String, ForeignKey('EC_numbers_tab.Id_ec'))
)


class Accessions(Base):  # le truc (Base) c'est l'héritage

    __tablename__ = "Accessions_tab"

    # Id = Column(Integer, primary_key=True, autoincrement=True)  # auto increment va gérer les id tt seul
    Id_access = Column(String, primary_key=True)

    #Les relations
    hasRefSeq = relationship("EC_numbers", secondary=association_table, back_populates="hasAcces")
    # hasPrimaire = relationship("EC_numbers", secondary=association_table)


class EC_numbers(Base):

    __tablename__ = "EC_numbers_tab"

    Id_ec = Column(String, primary_key=True)
    hasAcces = relationship("Accessions", secondary=association_table, back_populates="hasRefSeq") # mouais, mais hasprimaire alors?


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

    def ajout_access(self, param_access):
        ses.add(Accessions(Id_access=param_access))
        ses.commit()
        print("ajout_access fait!")

    def ajout_ec(self, param_num_ec):
        ses.add(EC_numbers(Id_ec=param_num_ec))
        ses.commit()

    def access_has_refeseq(self, param_id_access, param_list_ec):  #bon maintenant faut essayer d'update..
        # ses.add(Accessions(Id_access=param_id_access, hasRefSeq=param_list_ec))
        # ses.query("grande bzacterie1").update({Accessions.hasRefSeq: param_list_ec})
        selec = ses.query(Accessions).filter(Accessions.Id_access == param_id_access).one()
        selec.hasRefSeq += param_list_ec
        ses.add(selec)
        ses.commit()
        pass


# listAccessTruc = [EC_numbers(Id_ec="mechant num_ec10"), EC_numbers(Id_ec="mechant num_ec06")] #bon on peut pas dupliquer les nums ec ici..
listAccessTruc = [EC_numbers(Id_ec="mechant num_ec1111"), ses.query(EC_numbers).filter(EC_numbers.Id_ec == "mechantNum2").one()]
inst_remplissage = Remplissage()
# inst_remplissage.ajout_access("grande bzacterie1")
# inst_remplissage.ajout_access("grande bzacterie2")
# inst_remplissage.ajout_ec("mechantNum1")
# inst_remplissage.ajout_ec("mechantNum2")
# inst_remplissage.access_has_refeseq("grande bzacterie3", listAccessTruc)

####################################################################
"Requete sur les Tables "
####################################################################

class Requetes:

    def __init__(self):
        pass

    def print_table_access(self):
        resulAcc = ses.query(Accessions).all()
        for laccessin in resulAcc:
            print("ID de l'accession: ", laccessin.Id_access, sep=" ")
            for obj in laccessin.hasRefSeq:
                print(" Id du num EC: ", obj.Id_ec, end="", sep=" ")
            print("\n")
            pass

    def print_table_ecnum(self):
        resulEc = ses.query(EC_numbers).all()
        for laccessinBis in resulEc:
            print("ID du num EC: ", laccessinBis.Id_ec, sep=" ")
            listobjet = laccessinBis.hasAcces
            # print(listobjet)
            for obj in listobjet:
                print(" Id de l'access: ", obj.Id_access, end="")
            print("\n")
            pass

    def print_has_refseq(self, param_accession):
        resuRela = ses.query()  # boh en fait c'est a moitié déjà fait

    # print(association_table.c.Accessions_tab_id)

requetes = Requetes()  # instance de la classe requetes
requetes.print_table_access()
requetes.print_table_ecnum()
"""
ok ca marche parfaitement, les [] montrent les objets qui n'ont pas de relations, pour les autres
ca imprime entre [] les reférences des objets qu'il y a dans les relations. En plus c'est bien asymétrique
Plus qu'a trouver le moyen de faire des updates..
"""

####################################################################
"Requete sur les relations "
####################################################################


