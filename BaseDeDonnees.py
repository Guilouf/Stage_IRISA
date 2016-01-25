#!/usr/bin/env python
from sqlalchemy import *  # spécifier les imports (? pourquoi from?)

class BaseDDCl:
    """A quoi sert ce module de merde? Comme son nom l'indique, il crée une BDD
    bon alors ya deux trucs apparement, core et orm. Je ne sais pas trop lequel utiliser..
    tables.c.num_EC = tables.columns.get("num_EC")
    bon le truc est bien persistant, il se trouve à dans la racine! en.balec pr pas le commit
    """
    def __init__(self):
        """
        Initialise avec create_engine, se connecte à la bdd wesh
        """
        self.bdd = create_engine('sqlite:///test.balec', echo=True)  # crée ou ouvre bdd, ds la directory
        metadata = MetaData()  # bon c'est le type de schema..
        self.tables = Table('accession', metadata, Column('num_EC', String))  # les types de données sont en sql en gros

    def construction(self):

        """
        cree les tables
        :return: ?c'est quoi ca?
        """

        self.tables.create(self.bdd)  # on peut pas la créer a chaque fois.. faire gaffe à ca
        # tables.drop(bdd)  # pour la supprimer, on peut aussi utiliser drop_all comme create_all

    def insertion(self):
        """

        :return:
        """
        i = insert(self.tables)
        i = i.values({"num_EC": "bidu"})
        self.bdd.execute(i)

    def test(self):
        # @staticmethod ??
        """
        permet de tester si ca marche..
        """
        #connection = self.bdd.connect()
        #print(self.tables.c.num_EC)

        # en gros ca c du bon vieu sql, enfin presque

        # print(tables.c.num_EC.__dict__)  # c ou column aussi
        textquery = self.bdd.execute("SELECT num_EC FROM accession")
        for truc in textquery:
            print(truc)


if __name__ == "__main__":
    b = BaseDDCl()
    #b.construction()
    #b.insertion()
    b.test()
