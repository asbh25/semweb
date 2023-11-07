from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL ендпойнт
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# query для отримання пари одружених акторів, які разом знімалися у фільмах
query = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?actor1Name ?actor2Name
WHERE {
  ?film a dbo:Film ;
        dbo:starring ?actor1, ?actor2 .
  ?actor1 dbp:spouse ?actor2 .
  FILTER (?actor1 != ?actor2)

  ?actor1 rdfs:label ?actor1Name .
  ?actor2 rdfs:label ?actor2Name .
  FILTER (lang(?actor1Name) = 'en' && lang(?actor2Name) = 'en')
}
"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

results = sparql.query().convert()

for result in results["results"]["bindings"]:
    actor1Name = result["actor1Name"]["value"]
    actor2Name = result["actor2Name"]["value"]
    print(f"Family actors: {actor1Name} and {actor2Name}")
