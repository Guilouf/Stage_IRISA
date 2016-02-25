from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
"""
bon essayer sparqlwrapper2, qui envoit directe en json
Bien faire gaffe a ce que le uri correspondent au serv, et au données..
hum, parfois les prefixs se synchonisent mais pas les uri... SUR La vielle version de fusek, et apparement
Bon, a priori toutes les infos qui sont dans les sbml le serait dans mon rdf, reste a voir comment les retrouver..
"""
# TODO à synchro avec ma bdd des numéros ec (ya aussi des ec bizares, ac des | et des lettres..
# TODO relier les numéros ec du rdf aux accessions genbank, et aussi aux réseaux métaboliques et fichiers sbml

serveur = "http://localhost:3030/tgdbRDF"
sparql = SPARQLWrapper(serveur)
prefixes = """
prefix tgdb: <"""+serveur+"""/tgdb>
prefix metacyc: <"""+serveur+"""/metacyc>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""


class Query:
    """
    Essayer de retracer les classes metacyc, cad retrouver les mm résultats que le sbml
    """
    def __init__(self):
        pass

    listriple = ["#truc\n"]
    list_var = ["", "class", "nom"]  # la string vide c'est pour le join


    print(" ?".join([var for var in list_var]))


    sparql.setQuery("""
    """+prefixes+"""
    SELECT  """ + " ?".join([var for var in list_var]) + """
    WHERE {
        """ + "".join([tri for tri in listriple]) + """
        #?class a ?truc2 .
        #?class a metacyc:class .
        #?class rdfs:subClassOf tgdb:meta7325 .
        #?class metacyc:common_name ?nom .
        ?class a metacyc:class  .
        ?class metacyc:label ?nom .
        #rdf:guigui rdf:type ?nom .
    }
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        # print(result["class"]["value"], end=" ")  # le end pour ne pas sauter de lignes
        print(result["nom"]["value"])

# Query


class Update:
    """
    Insérer les données de ma bdd des numéros ec
    """
    sparql.setQuery("""
    """+prefixes+"""

    INSERT DATA {
        rdf:guigui rdf:type "genie"  .
    }
    """)
    sparql.method = 'POST'
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    print(result)

# Update
