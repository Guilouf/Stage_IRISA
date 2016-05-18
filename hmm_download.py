from Bio import Entrez, SeqIO
from urllib.request import *
from urllib.parse import *


"""
http://www.uniprot.org/help/programmatic_access
On récupère via le site les identifiants car j'y arrive pas avec l'api..
Pour le
"""

























"""
def recup_uni_strai_acc(param_list_id):
    list_id = param_list_id
    url = "http://www.uniprot.org/mapping/"
    # faut mettre " au lieu de ' dans la partie requete

    # alors ACC+ID ca marche pas hein, quoi qu'ils disent
    params = {
        'from': 'P_GI',
        'to': 'ACC',  # id est plus long, mais apporte pas d'info par rapport à acc. C'est acc dans metacyc..
        'format': 'tab',
        # 'query': " ".join([id for id in list_id])
        'query': "489222426"
    }

    data = urlencode(params).encode('utf-8')
    request = Request(url, data)

    try:
        response = urlopen(request, timeout=50)
    except:
        print("Deuxième essai bdd ****")
        time.sleep(20)
        try:
            response = urlopen(request, timeout=50)
        except:
            print("3eme essai bdd de ***")
            time.sleep(30)
            response = urlopen(request, timeout=50)

    # pourrait faire un yield
    return [line.decode('utf-8') for line in response]


with open('Exemple/ListeAccess', 'r') as fich_list__acc_ncbi:
    list__acc_ncbi = [li.strip() for li in fich_list__acc_ncbi]
    # recup_uni_strai_acc(list__acc_ncbi)
    for i in recup_uni_strai_acc(['NZ_CP009472.1']):
        print(i)

"""