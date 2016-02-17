from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
"""
bon essayer sparqlwrapper2, qui envoit directe en json
"""
serveur = "http://localhost:3030/tgdbRDF"


sparql = SPARQLWrapper(serveur)


sparql.setQuery("""
prefix tgdb: <"""+serveur+"""/tgdb>
prefix metacyc: <"""+serveur+"""/metacyc>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT  ?class
WHERE {
    #?truc rdfs:type ?class .
    ?class a metacyc:class
}
""")


""
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["class"]["value"])
""