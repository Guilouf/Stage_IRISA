#!/usr/bin/env python
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationships

eng = create_engine('sqlite:///testBis.balec')

Base = declarative_base()

class Accessions(Base):  # le truc (Base) c'est l'héritage

    __tablename__ = "Accessions_tab"

    Id = Column(Integer, primary_key=True)
    Access = Column(String)

    #hasRefSeq = relationships('Friends', primaryjoin=lambda: id == EC_numbers.Id_ec)
    hasRefSeq = relationships()


class EC_numbers(Base):

    __tablename__ = "EC_numbers_tab"

    Id_ec = Column(Integer, primary_key=True)
    num_ec = column(String)

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

"""
ses.add(Accessions(Id=2, Access="grande bzacterie"))
ses.commit()
"""

resul = ses.query(Accessions).all()

for laccessin in resul:
    print(laccessin.Access)