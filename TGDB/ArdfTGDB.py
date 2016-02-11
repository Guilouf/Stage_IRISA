# -*- coding: utf-8 -*-


#from lib.tinygraphdbplus import Tinygraphdbplus
from tinygraphdb import Tinygraphdb


tgdb = Tinygraphdb("tgdbRef.tgdb")





#print(tgdb.getDicOfNode())

def printnodes():
    gen_all_keys = (node.getMisc().keys() for node in tgdb.getDicOfNode().values())
    all_keys = set()

    for i in gen_all_keys:

        i = set(i)

        all_keys = all_keys.union(i)

    print(all_keys)
    print(type(all_keys))

# printnodes()

for i in tgdb.getDicOfNode():
    # print(i)  # ca print le nom du noeud,un string donc
    pass


def attrnodes():
    for i in tgdb.getDicOfNode().values():
        # print(i)  # print l'adress mem de l'objet
        print(i.getMisc())
        print(i.getClass())  # renvoit le nom de la classe
        print(i.getId())
# attrnodes()


for i in tgdb.getTuplOfRelation():  # c'est un tupe
    # print(i.getIdIn())
    # print(i.getIdOut())
    print(i.getType())
    pass