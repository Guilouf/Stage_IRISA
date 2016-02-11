# -*- coding: utf-8 -*-


#from lib.tinygraphdbplus import Tinygraphdbplus
from tinygraphdb import Tinygraphdb

class TgdbToRDF:
    """
    alors je pourrai faire un truc classe et lisible en ne mettant que des doublets après avoir déclaré le premier truc,
    mais comme c'est plus simple je vais pour l'instant faire crade.
    J'ai l'impression que son truc me sort de l'aléatoire...
    """


    def __init__(self):
        self.tgdb = Tinygraphdb("tgdbRef.tgdb")

        self.fich_sortie = open("tgdbSortie.balec", 'w+')  # faire un with open ac la func principale dedans

        # écrire les préfixes dans le init
        # TODO mettre les points à la fin... ou faire des triplets complets

    @staticmethod
    def rectif_stochio(dicoSto, idmetaparam): #renvoit la liste d'identifiants bis à la place de la stochio
        stochio = dicoSto["stoichiometry"][0]  # TODO etre sur qu'il n'y ait qu'une clé, ce serait pas la première surprise
        # TODO au fait ca ne sert que si la stochio est sup à 1...
        # et qu'une seule valeur...

        def gener_ident_bis(stochioint, idmetaparam):
            list_ident = []
            if stochioint == 1:  # si stochio à un, on retourne l'id de base
                return [idmetaparam.lower()]
            for num in range(stochioint):
                list_ident.append(idmetaparam.lower()+"b"+str(num))
            return list_ident

        if stochio.isdigit():  # detecte si c un nombre
            return gener_ident_bis(int(stochio), idmetaparam)
        elif stochio == 'n':
            return gener_ident_bis(1, idmetaparam)
        elif stochio == "n+1":
            return gener_ident_bis(2, idmetaparam)
        elif stochio == "(n+1)":
            return gener_ident_bis(2, idmetaparam)
        elif stochio == "2n":
            return gener_ident_bis(2, idmetaparam)

    def nodes_to_rdf(self):
        for node in self.tgdb.getDicOfNode().values():
            print("/!\ID du noeud:      ", node.getId())  # tgdb:"lid du truc"
            str_node = "tgdb:"+node.getId().lower()

            self.fich_sortie.write(str_node+" a metacyc:"+node.getClass()+" .\n")  # crée le nom du noeud et sa class

            dicomisc = node.getMisc()
            for key in dicomisc.keys():  # impression du misc
                print(key)
                self.fich_sortie.write(str_node+"\t"+"metacyc:"+key+'\t"'+str(dicomisc[key][0])+'"'+" .\n")
                # /!\/!\/!\ les valeurs sont des listes.. je ne sais pas si ya plusieurs valeurs parfois
                # TODO faire un avertissment si ya des listes de plus de 1, genre un assert
                # print(dicomisc[key])

            """
            if dicomisc is not None:
                TgdbToRDF.write_misc(dicomisc)  # ecrit le misc du noeud
            """

            relations_tpl = self.tgdb.getRelation(node.getId(), "in")  # renvoit un tuple des relations, none sinon..
            dico_pr_stochio = {}  #dico pr stocker les stochio associé au clés id
            if relations_tpl is not None:
                for rel in relations_tpl:
                    print(rel.getType())
                    if rel.getType() == "is a":
                        self.fich_sortie.write(str_node+"\t"+"rdfs:subClassOf\t"+"tgdb:"+rel.getIdOut().lower()+" .\n")

                    elif rel.getType() == "produces" or rel.getType() == "consumes":  #pour les stochios
                        # TODO pas oublier catalyse...

                        valeur_sto_recti = TgdbToRDF.rectif_stochio(rel.getMisc(), rel.getIdOut())  # c une liste
                        for ident_recti in valeur_sto_recti:
                            self.fich_sortie.write(str_node+"\t"+"tgdb:"+rel.getType()+" "+"tgdb:"+ident_recti+" .\n")
                            pass

                        dico_pr_stochio[rel.getIdOut()] = valeur_sto_recti  #on charge dans le dico
                        # TODO attention c plutot getidout() (ok mais verif)

                        pass
                    else:
                        self.fich_sortie.write(str_node+"\t"+"tgdb:"+rel.getType().replace(" ", "")+"\ttgdb:"+rel.getIdOut().lower()+" .\n")
                    pass

            # ecriture des ref la stochiometrie
            for key in dico_pr_stochio:
                for ident_b in dico_pr_stochio[key]:
                    if len(dico_pr_stochio[key]) > 1 :  # ca sert à rien d'écrire si l'ident pas modif..
                        self.fich_sortie.write("tgdb:"+ident_b.lower()+" a\t"+"tgdb:"+key.lower()+" .\n")
                        # todo un for de trop...

            self.fich_sortie.flush()  # pour decharger le buffer avant le kbinterupt
            # TODO enlever le flush une fois mis au point


"""
    # fait chier connerie de merde!!!!!!!!!!!!!!!!!!!!!
    # @staticmethod
    def write_misc(self, dicomiscparam):
        print("merde")
        for key in dicomiscparam.keys():
            print(key)
            self.fich_sortie.write("metacyc:")
            pass
"""

inst = TgdbToRDF()
inst.nodes_to_rdf()

##################################################################
# test pour la stochio
##################################################################
"""
tgdb = Tinygraphdb("tgdbRef.tgdb")
rel_tpl = tgdb.getRelation("META52053", "in")  # renvoit un tuple

def rectif_stochio(dicoSto,idmetaparam): #renvoit la liste d'identifiants bis à la place de la stochio
    stochio = dicoSto["stoichiometry"][0]  # TODO etre sur qu'il n'y ait qu'une clé, ce serait pas la première surprise
    # TODO au fait ca ne sert que si la stochio est sup à 1...
    # et qu'une seule valeur...

    def gener_ident_bis(stochioint, idmetaparam):
        list_ident = []
        for num in range(stochioint):
            list_ident.append(idmetaparam.lower()+"B"+str(num))
        return list_ident

    if stochio.isdigit():  # detecte si c un nombre
        return gener_ident_bis(int(stochio), idmetaparam)
    elif stochio == 'n':
        return gener_ident_bis(1, idmetaparam)
    elif stochio == "n+1":
        return gener_ident_bis(2, idmetaparam)
    elif stochio == "(n+1)":
        return gener_ident_bis(2, idmetaparam)
    elif stochio == "2n":
        return gener_ident_bis(2, idmetaparam)



dico_pr_stochio = {}
for rel in rel_tpl:
    print(rel.getType())
    # /!\/!\/!\if rel.getType() == ("produces" or "consumes"):  #pour les stochios TODO pourquoi mais pourquoi BORDEL???
    if rel.getType() == "produces" or rel.getType() == "consumes":
        # fich_sortie.write("tgdb:"+rel.getType().replace(" ", "")+"\ttgdb:"+rel.getIdOut().lower()+";\n")
        print("merde")
        print(rel.getMisc())
        valeur_sto_recti = rectif_stochio(rel.getMisc(), rel.getIdOut())
        dico_pr_stochio[rel.getIdOut()] = valeur_sto_recti

print(dico_pr_stochio)
"""






# TODO crise de larmes
"""
plusieurs possibilités de stochio: la classique, un chiffre. L'originale, un n. (META48933)
l'extravagante, n+1 (META48942), la subversive, (n+1) (META52053), et la salope: 2n (META52053)(encore..)
"""

"""
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
        pass
# attrnodes()


for i in tgdb.getTuplOfRelation():  # c'est un tuple
    # print(i)
    # print(i.getIdIn())  # avec ca on peut chopper ce qui m'interesse
    # print(i.getIdOut())
    # print(i.getType())
    pass

# pour retrouver une relation:
rel = tgdb.getRelation("META22465", "in")  # renvoit un tuple

for i in rel:
    print(i.getType())
"""