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

        # c'est bien un pb de timeout, ou de 503 unavailable
        # je pourrai faire un try except, ou faire un fake user agent
        # ou un time sleep puis un retry..
        self.page = (line.decode('utf-8') for line in response)

    def print_resul(self):
        print(self.page)

    # TODO attention au générateur, c'est pe à cause de ca les EC en trop.. ouais
    # todo pour après: stocker les identifiants dans une liste
    # todo solution: en position 0 se trouve le num Gi, continue!!
    def gener_id(self):
        header = next(self.page)  # sert à rien ca ??
        # gener_gi = (gi for gi in self.list_id)
        gener_page = (ligne for ligne in self.page)

        for gi in self.list_id:
            for ligne in gener_page:
                if ligne.split('\t')[0] == gi:
                    yield ligne.split('\t')[1].strip()
                    break

# ['917680677', '917680578']
# print(next(Uniprot(['917680677']).gener_id()))

#
# generateur = Uniprot(['917680677', '296920967', '489740567']).gener_id()
#
# for i in range(0, 10):
#     print(next(generateur))

