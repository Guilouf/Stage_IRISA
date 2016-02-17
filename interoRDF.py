from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
"""
bon essayer sparqlwrapper2, qui envoit directe en json
"""
sparql = SPARQLWrapper("http://localhost:3030/tgdbRDF")


sparql.setQuery("""
prefix tgdb: <http://localhost:3030/essaiTGDB/tgdb>
prefix metacyc: <http://localhost:3030/essaiTGDB/metacyc>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT  ?class
WHERE {
    #?truc rdfs:type ?class .
    ?class a metacyc:class
}
""")


# for i in sparql.query().fullResult:
#     print(i)

""
sparql.setReturnFormat(JSON)
results = sparql.query().convert()



for result in results["results"]["bindings"]:
    print(result["class"]["value"])
""