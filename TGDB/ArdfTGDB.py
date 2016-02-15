# -*- coding: utf-8 -*-

# from lib.tinygraphdbplus import Tinygraphdbplus
from tinygraphdb import Tinygraphdb


class TgdbToRDF:
    """
    J'ai l'impression que son truc me sort de l'aléatoire...
    Pour les assignement, apparement il peut y avoir un truc de type "assignment	X	score	Y", mais pas observé
    dans le tgdb donc laissé tel quel pr l'instant.
    """

    def __init__(self):
        self.tgdb = Tinygraphdb("tgdbRef.tgdb")

        self.tgdb_nodes = (node for node in self.tgdb.getDicOfNode().values())  # générateur de noeuds TODO inutile ca en fait, et p e dangereux
        self.tgdb_rel = (rel for rel in self.tgdb.getTuplOfRelation())

        self.dico_rel = {}

        for rel in self.tgdb_rel:  # opti de ouf
            idin = rel.getIdIn()
            clefs = self.dico_rel.keys()
            if idin in clefs:
                self.dico_rel[rel.getIdIn()] += (rel,)
            else:
                self.dico_rel[rel.getIdIn()] = (rel,)


        self.fich_sortie = open("tgdbSortie.balec", 'w+', encoding="utf-8")  # pas de close, mais balec

        # le saut de ligne genere des tabs.. c normal crétin, tu prend les tabs de l'éditeur comme texte...
        self.fich_sortie.write("# metacyc: les qualifiants directes des noeuds\n"\
            "# tgdb: les entites(noeuds) et les relations\n" \
            + "# rdf:type la classe metacyc du noeud(feuille); rdfs:subClassOf la superclasse de noeud\n" \
            + "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n" \
            + "@prefix tgdb:  <http://localhost:3030/essaiTGDB/tgdb> .\n" \
            + "@prefix metacyc: <http://localhost:3030/essaiTGDB/metacyc> .\n" \
            + "@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n")

    @staticmethod
    def rectif_stochio(dicoSto, idmetaparam):  # renvoit la liste d'identifiants bis à la place de la stochio
        stochio = dicoSto["stoichiometry"][0]  # TODO etre sur qu'il n'y ait qu'une clé, ce serait pas la première surprise
        # TODO au fait ca ne sert que si la stochio est sup à 1...(c'est fait)
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
        elif stochio == 'n': # TODO ca c 1, voir plus haut..
            return gener_ident_bis(1, idmetaparam)
        elif stochio == "n+1":
            return gener_ident_bis(2, idmetaparam)
        elif stochio == "(n+1)":
            return gener_ident_bis(2, idmetaparam)
        elif stochio == "2n":
            return gener_ident_bis(2, idmetaparam)
        else: return gener_ident_bis(0, idmetaparam)  # TODO faire qq chose pour les n bizares...

    def nodes_to_rdf(self):
        cpt_node = 0  # compteur de nombre de noeud parcouru, utilisé pour le flush TODO asuppr
        for node in self.tgdb_nodes:  # itere le générateur
            print("/!\ID du noeud:      ", node.getId())  # tgdb:"lid du truc"
            str_node = "tgdb:"+node.getId().lower()  # le sujet, cad le noeud

            cpt_node += 1  # incre du compteur de noeud TODO asuppr
            self.fich_sortie.write(str_node+" a metacyc:"+node.getClass()+" .\n")  # ecrit le nom du noeud et sa class

            # impression du misc
            dicomisc = node.getMisc()
            for key in dicomisc.keys():  # /!\/!\/!\ les valeurs sont des listes.. META51128=>multiple
                print("VALEUR DE CLE MULTIPLE") if len(dicomisc[key]) > 1 else None  # ternaire pr test multi val
                for value in dicomisc[key]:  # les valeurs des clef sont des listes...
                    self.fich_sortie.write(str_node+"\t"+"metacyc:"+key.replace(" ", "")+'\t"'+value+'"'+" .\n")

            relations_tpl = self.dico_rel.get(node.getId(), None)

            dico_pr_stochio = {}  # dico pr stocker les stochio associé au clés id
            if relations_tpl is not None:  # test si le noeud possède bien des relations
                for rel in relations_tpl:  # parcourt les relations que possede le noeud


                    if rel.getType() == "is a":  # pour le cas des sous classes
                        self.fich_sortie.write(str_node+"\t"+"rdfs:subClassOf\t"+"tgdb:"+rel.getIdOut().lower()+" .\n")

                    elif rel.getType() in ("produces", "consumes"):  # pour les stochios
                        # TODO pas oublier catalyse (en fait non, ya pas de stochio associé)

                        valeur_sto_recti = TgdbToRDF.rectif_stochio(rel.getMisc(), rel.getIdOut())  # c une liste, parfois none qd erreur genre 4n
                        for ident_recti in valeur_sto_recti:
                            self.fich_sortie.write(str_node+"\t"+"tgdb:"+rel.getType()+" "+"tgdb:"+ident_recti+" .\n")

                        dico_pr_stochio[rel.getIdOut()] = valeur_sto_recti  # on charge dans le dico

                    else:  # pour les autres relations, hasname etc...
                        self.fich_sortie.write(str_node+"\t"+"tgdb:"+rel.getType().replace(" ", "")+"\ttgdb:"\
                                               + rel.getIdOut().lower()+" .\n")
                        if len(rel.getMisc()) != 0:  # pour ajouter les assignements (si yen a)
                            assign = rel.getMisc()["assignment"]
                            self.fich_sortie.write(str_node+"\t"+"tgdb:hasassign"\
                                                   + "\ttgdb:"+assign[0].lower()+" .\n")

            # ecriture des ref la stochiometrie
            self.write_stochio(dico_pr_stochio)

            if (cpt_node / 100)%1 == 0:  # tous les 100 itérations
                self.fich_sortie.flush()  # pour decharger le buffer avant le kbinterupt
                print("flush!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(cpt_node)
            # TODO sert plus vraiment le flush

    def write_stochio(self, dico_pr_stochio_pr):
        for key in dico_pr_stochio_pr:
                for ident_b in dico_pr_stochio_pr[key]:
                    if len(dico_pr_stochio_pr[key]) > 1:  # ca sert à rien d'écrire si l'ident pas modif..
                        self.fich_sortie.write("tgdb:"+ident_b.lower()+" a\t"+"tgdb:"+key.lower()+" .\n")

inst = TgdbToRDF()
inst.nodes_to_rdf()

"""
tgdb = Tinygraphdb("tgdbRef.tgdb")

tgdb_nodes = (node for node in tgdb.getDicOfNode().values())  # générateur de noeuds
tgdb_rel = (rel for rel in tgdb.getTuplOfRelation())  # retourne un tuple d'objets. le get in est le truc a recupérer.

dico_rel = {}

for rel in tgdb_rel:
    idin = rel.getIdIn()
    clefs = dico_rel.keys()
    if idin in clefs:
        dico_rel[rel.getIdIn()] += (rel,)
    else:
        dico_rel[rel.getIdIn()] = (rel,)

print("fini_dico_rel!!!")
print(dico_rel["META2268"])

# tgdb_rel()
# for rel in tgdb_rel:
#     print(rel.getIdOut())

"""
##################################################################
# test pour la stochio
##################################################################
"""
# TODO crise de larmes

plusieurs possibilités de stochio: la classique, un chiffre. L'originale, un n. (META48933)
l'extravagante, n+1 (META48942), la subversive, (n+1) (META52053), et la salope: 2n (META52053)(encore..)
sournoise! |2n| !!!

# pour retrouver les différentes clés

def printnodes():
    gen_all_keys = (node.getMisc().keys() for node in tgdb.getDicOfNode().values())
    all_keys = set()

    for i in gen_all_keys:

        i = set(i)

        all_keys = all_keys.union(i)

    print(all_keys)
    print(type(all_keys))

"""