from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
"""
bon essayer sparqlwrapper2, qui envoit directe en json
Bien faire gaffe a ce que le uri correspondent au serv, et au données..
hum, parfois les prefixs se synchonisent mais pas les uri... SUR La vielle version de fusek, et apparement
pas d'impact sur les resultats. => en fait il additionne les triples on dirait
"""
serveur = "http://localhost:3030/tgdbRDF"


sparql = SPARQLWrapper(serveur)
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
    ?class rdfs:subClassOf tgdb:meta7325 .
    ?class metacyc:common_name ?nom .
}
""")


sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["class"]["value"], end="")  # le end pour ne pas sauter de lignes
    print(result["nom"]["value"])
