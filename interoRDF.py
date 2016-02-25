from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
"""
bon essayer sparqlwrapper2, qui envoit directe en json
Bien faire gaffe a ce que le uri correspondent au serv, et au données..
hum, parfois les prefixs se synchonisent mais pas les uri... SUR La vielle version de fusek, et apparement
"""
# TODO à synchro avec ma bdd des numéros ec (ya aussi des ec bizares, ac des | et des lettres..
# TODO relier les numéros ec du rdf aux accessions genbank, et aussi aux réseaux métaboliques et fichiers sbml

serveur = "http://localhost:3030/tgdbRDF"
sparql = SPARQLWrapper(serveur)


class Query:

    listriple = ["#truc\n"]
    list_var = ["", "class", "nom"]  # la string vide c'est pour le join


    print(" ?".join([var for var in list_var]))


    sparql.setQuery("""
    prefix tgdb: <"""+serveur+"""/tgdb>
    prefix metacyc: <"""+serveur+"""/metacyc>
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT  """ + " ?".join([var for var in list_var]) + """
    WHERE {
        """ + "".join([tri for tri in listriple]) + """
        #?class a ?truc2
        #?class a metacyc:class
        #?class rdfs:subClassOf tgdb:meta7325 .
        #?class metacyc:common_name ?nom .
        #?class metacyc:ec ?nom
        rdf:guigui rdf:type ?nom
    }
    """)


    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        # print(result["class"]["value"], end=" ")  # le end pour ne pas sauter de lignes
        print(result["nom"]["value"])

# Query


serveur = "http://localhost:3030/tgdbRDF"
sparql2 = SPARQLWrapper(serveur)


class Update:
    sparql2.method = 'POST'
    sparql2.setQuery("""
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    INSERT DATA {
        rdf:guigui rdf:type "genie"  .
    }
    """)
    sparql2.method = 'POST'
    sparql2.setReturnFormat(JSON)
    result = sparql2.query().convert()
    print(result)

# Update
