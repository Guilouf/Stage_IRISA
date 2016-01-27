#!/usr/bin/env python
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

eng = create_engine('sqlite:///testBis.balec')

Base = declarative_base()

# Table d'association
association_table = Table('association', Base.metadata,
    Column('Accessions_tab_id', Integer, ForeignKey('Accessions_tab.Id')),
    Column('EC_numbers_tab_id', Integer, ForeignKey('EC_numbers_tab.Id_ec'))
)

class Accessions(Base):  # le truc (Base) c'est l'héritage

    __tablename__ = "Accessions_tab"

    Id = Column(Integer, primary_key=True)
    Access = Column(String)

    #les relations
    hasRefSeq = relationship("EC_numbers", secondary=association_table, back_populates="hasAcces")
    # hasPrimaire = relationship("EC_numbers", secondary=association_table)


class EC_numbers(Base):

    __tablename__ = "EC_numbers_tab"

    Id_ec = Column(Integer, primary_key=True)
    num_ec = Column(String)
    hasAcces = relationship("Accessions", secondary=association_table, back_populates="hasRefSeq") # mouais, mais hasprimaire alors?
    # backref ou back populate?,


"""
class RefSeq(Base):  # bug avec le base ici

    __tablename__ = "RefSeq_tab"

    col_accession = Column(String, ForeignKey(Accessions.Id))
    col_ec = Column(String, ForeignKey(EC_numbers.Id_ec))

class Primaire:

    __tablename__ = "Primaire_tab"

    col_accession = Column(String)
    col_ec = Column(String)
"""

Base.metadata.bind = eng
Base.metadata.create_all()

Session = sessionmaker(bind=eng)
ses = Session()

####################################################################
"Remplissages des tables"
####################################################################
# ses.add(Accessions(Id=0, Access="grande bzacterie0"))
# ses.commit()
#
# ses.add(EC_numbers(Id_ec=1, num_ec="mechant num_ec1"))
# ses.commit()

# Relations: ok putain ca marche un peu..
# deuximeEC = EC_numbers(Id_ec=13, num_ec="mechant num_ec13")
# ses.add(Accessions(Id=4, hasRefSeq=[EC_numbers(Id_ec=12, num_ec="mechant num_ec11"),deuximeEC]))
# ses.commit()
####################################################################
"Requete sur les Tables "
####################################################################
resulAcc = ses.query(Accessions).all()
resulEc = ses.query(EC_numbers).all()
# resuRela = ses.query()

for laccessin in resulAcc:
    # print(laccessin.Id)
    # print(laccessin.Access)
    print(laccessin.hasRefSeq)
    pass

for laccessinBis in resulEc:
    # print(laccessinBis.Id_ec)
    # print(laccessinBis.num_ec)
    listobjet = laccessinBis.hasAcces
    print(listobjet)
    for obj in listobjet:
        print(obj.Id)
    pass

print(association_table.c.Accessions_tab_id)
"""
ok ca marche parfaitement, les [] montrent les objets qui n'ont pas de relations, pour les autres
ca imprime entre [] les reférences des objets qu'il y a dans les relations. En plus c'est bien asymétrique
Plus qu'a trouver le moyen de faire des updates..
"""

####################################################################
"Requete sur les relations "
####################################################################


