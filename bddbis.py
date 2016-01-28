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
    Column('Accessions_tab_id', Integer, ForeignKey('Accessions_tab.Id')),
    Column('EC_numbers_tab_id', Integer, ForeignKey('EC_numbers_tab.Id_ec'))
)

Base.metadata.bind = eng
Base.metadata.create_all()

Session = sessionmaker(bind=eng)
ses = Session()


class Accessions(Base):  # le truc (Base) c'est l'héritage

    __tablename__ = "Accessions_tab"

    Id = Column(Integer, primary_key=True, autoincrement=True)  # auto increment va gérer les id tt seul
    Access = Column(String)

    #les relations
    hasRefSeq = relationship("EC_numbers", secondary=association_table, back_populates="hasAcces")
    # hasPrimaire = relationship("EC_numbers", secondary=association_table)


class EC_numbers(Base):

    __tablename__ = "EC_numbers_tab"

    Id_ec = Column(Integer, primary_key=True, autoincrement=True)
    num_ec = Column(String)
    hasAcces = relationship("Accessions", secondary=association_table, back_populates="hasRefSeq") # mouais, mais hasprimaire alors?
    # backref ou back populate?,


####################################################################
"Remplissages des tables"
####################################################################


class Remplissage:

    def __init__(self):
        pass

    def ajout_access(self, param_access):
        ses.add(Accessions(Access=param_access))
        ses.commit()
        print("ajout_access fait!")

    def ajout_ec(self):
        ses.add(EC_numbers(num_ec="mechant num_ec1"))
        ses.commit()

    def access_has_refeseq(self):
        deuximeEC = EC_numbers(num_ec="mechant num_ec13")
        ses.add(Accessions(hasRefSeq=[EC_numbers(num_ec="mechant num_ec11"),deuximeEC]))
        ses.commit()
        pass

inst_remplissage = Remplissage()
inst_remplissage.ajout_access("grande bzacterie1")
inst_remplissage.ajout_access("grande bzacterie2")

####################################################################
"Requete sur les Tables "
####################################################################

class Requetes:

    def __init__(self):
        pass

    def print_table_access(self):
        resulAcc = ses.query(Accessions).all()
        for laccessin in resulAcc:
            # print(laccessin.Id)
            # print(laccessin.Access)
            print(laccessin.hasRefSeq)
            pass

    def print_table_ecnum(self):
        resulEc = ses.query(EC_numbers).all()
        for laccessinBis in resulEc:
            # print(laccessinBis.Id_ec)
            # print(laccessinBis.num_ec)
            listobjet = laccessinBis.hasAcces
            print(listobjet)
            for obj in listobjet:
                print(obj.Id)
            pass

    def print_has_refseq(self, param_accession):
        resuRela = ses.query()

    print(association_table.c.Accessions_tab_id)

requetes = Requetes()  # instance de la classe requetes
requetes.print_table_access()
"""
ok ca marche parfaitement, les [] montrent les objets qui n'ont pas de relations, pour les autres
ca imprime entre [] les reférences des objets qu'il y a dans les relations. En plus c'est bien asymétrique
Plus qu'a trouver le moyen de faire des updates..
"""

####################################################################
"Requete sur les relations "
####################################################################


