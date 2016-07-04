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
        # todo ouais ben pas si beau que ca refait..
        try:
            response = urlopen(request, timeout=50)
        except:
            print("Deuxième essai!")
            time.sleep(20)
            try:
                response = urlopen(request, timeout=50)
            except:
                print("3eme essai!")
                time.sleep(30)
                response = urlopen(request, timeout=50)


        self.page = [line.decode('utf-8') for line in response]
        # self.page = (line.decode('utf-8') for line in response)
        # self.result_test = [line_.decode('utf-8') for line_ in response]  # ok, ca epuise self.page, qu'on m'explique.. c'est vide

    def print_resul(self):
        print(self.page)

    # TODO faut gérer ceux qui ne peuvent pas être mappés..Y aurait il un problème de répétition de GI? (NC_017486.1)
    # TODO sauf ceux qui sont collés à la suite qui devrait avoir une ref différente, pas si grave.
    def gener_id(self):
        """
        permet de ne retenir que le premier résultat de cross ref par numéro GI, en épuisant les resultats
        suivants.
        :return:
        """

        # header = next(self.page)  # sert à rien ca ??(dégager les header pe
        gener_page = (ligne for ligne in self.page)  # fait un générateur de la page de résultats

        for gi in self.list_id:  # défile les numeros gi de la liste
            for ligne in gener_page:  # itere le générateur des resultats
                # print("linge_gener: ", ligne)
                if ligne.split('\t')[0] == gi:  # a chaque match entre le numero GI de la liste et de la page resultat
                    # print("ligne_yield: ", ligne)
                    yield ligne.split('\t')[1].strip()
                    break  # hum, ca break quoi exactement?


