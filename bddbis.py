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
    hasRefSeq = relationship("EC_numbers", secondary=association_table)
    hasPrimaire = relationship("EC_numbers", secondary=association_table)


class EC_numbers(Base):

    __tablename__ = "EC_numbers_tab"

    Id_ec = Column(Integer, primary_key=True)
    num_ec = Column(String)

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
# ses.add(Accessions(Id=3, Access="grande bzacterie3"))
# ses.commit()

# ses.add(EC_numbers(Id_ec=3, num_ec="mechant num_ec3"))
# ses.commit()

# Relations:
# Accessions.hasRefSeq(EC_numbers(Id_ec=3))

####################################################################
"Requete sur les Tables "
####################################################################
resulAcc = ses.query(Accessions).all()
resulEc = ses.query(EC_numbers).all()

for laccessin in resulAcc:
    print(laccessin.Id)
    print(laccessin.Access)

for laccessinBis in resulEc:
    print(laccessinBis.Id_ec)
    print(laccessinBis.num_ec)

####################################################################
"Requete sur les relations "
####################################################################


