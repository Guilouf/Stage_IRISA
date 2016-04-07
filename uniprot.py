import time
from urllib.request import *
from urllib.parse import *

"""
http://www.uniprot.org/help/programmatic_access
"""


class Uniprot:

    def __init__(self, list_id):
        self.list_id = list_id
        url = "http://www.uniprot.org/mapping/"


        params = {
            'from': 'P_GI',
            'to': 'ACC',  # id est plus long, mais apporte pas d'info par rapport à acc. C'est acc dans metacyc..
            'format': 'tab',
            'query': " ".join([id for id in self.list_id])
        }

        data = urlencode(params).encode('utf-8')
        request = Request(url, data)

        # un beau try except recursif..
        try:
            response = urlopen(request, timeout=50)
        except:
            print("Deuxième essai bdd de merde!")
            time.sleep(20)
            try:
                response = urlopen(request, timeout=50)
            except:
                print("3eme essai bdd de merde!")
                time.sleep(30)
                response = urlopen(request, timeout=50)


        self.page = [line.decode('utf-8') for line in response]
        # self.page = (line.decode('utf-8') for line in response)
        # self.result_test = [line_.decode('utf-8') for line_ in response]  # ok, ca epuise self.page, qu'on m'explique..

    def print_resul(self):
        print(self.page)

    # TODO faut gérer ceux qui ne peuvent pas être mappés..Y aurait il un problème de répétition de GI? (NC_017486.1) apparement non il gère les doublons
    # TODO sauf ceux qui sont collés à la suite qui devrait avoir une ref différente, pas si grave.
    def gener_id(self):
        """
        permet de ne retenir que le premier résultat de cross ref par numéro GI, en épuisant les resultats
        suivants.
        :return:
        """
        # /!\/!\/!\ self.page est(ait) un putain de générateur..
        # header = next(self.page)  # sert à rien ca ??(dégager les header pe
        gener_page = (ligne for ligne in self.page)  # fait un générateur de la page de résultats

        for gi in self.list_id:  # défile les numeros gi de la liste
            for ligne in gener_page:  # itere le générateur des resultats
                print(ligne.split('\t')[1].strip())
                if ligne.split('\t')[0] == gi:  # a chaque match entre le numero GI de la liste et de la page resultat
                    yield ligne.split('\t')[1].strip()
                    break  # hum, ca break quoi exactement?

        """
        GROS DEBUG
        enfin une piste: 489221419, 2 occurences trouvées.. quels batards. mm caractéristiques ds le gbk
        ce qu'est bizare c'est que pour les doublons simulés ca passe..
        =>en fait c'est sur le suivant que ca fait foirer.. donc c'est bien la faute des doublons
        """

        print("test de debug")
        for gi in self.list_id:
            present = False
            for ligne in self.page:
                if ligne.split('\t')[0] == gi:
                    # print("ref_resul: ", ligne.split('\t')[0])
                    # print("num_gi: ", gi)  # c'est normal qu'il y ait plusieur matchs, c pr les ref multiples
                    present = True
            if present == False:
                print("PB§§§", gi)


# TODO dès qu'un truc ne match pas, le générateur s'épuise.(pas si sur) itertools pr 2eme générateur
# TODO voir du coté de recup ec, au niveau de la longeur du for..

# ['917680677', '917680578']
# print(next(Uniprot(['917680677']).gener_id()))

# list_test = ['489221419', '917680578', '917680677', '489221419', '490375107']
list_test = ['917680578', '917680578', '917680677', '490375162', '917680578', '490375107']
# list_test = ['489221419', '917680578', '917680677', '490375162', '490375107', '490374849', '489221547', '489221419'
#              , '504383723']
generateur = Uniprot(list_test).gener_id()
#
for i in range(0, len(list_test)):
    print(next(generateur))

"""
raaaaaaaaaaahhhhhhaaaaaaaaaaa ais pourquoi putain ca marfche aussedesss et pas la bordel de chiiotore!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# with open("Test/debugRecup.txt", 'r') as list_gigo:
#     list_strip = [gi.strip() for gi in list_gigo]
#     generateur = Uniprot(list_strip).gener_id()
#     for i in range(0, len(list_strip)):
#         print(next(generateur))
