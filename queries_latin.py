LILA_ENDPOINT  = "https://lila-erc.eu/sparql/"

GET_WORDNET_LEXICAL_ENTRIES = """
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT * WHERE {
  ?s a ontolex:LexicalEntry .
  ?s rdfs:label ?o .
  FILTER (strstarts(str(?s), "http://lila-erc.eu/data/lexicalResources/LatinWordNet"))
} 
"""

GET_DOCUMENTS_BY_TITLE = """
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX powla: <http://purl.org/powla/powla.owl#>

SELECT ?doc ?pred ?title WHERE {
  ?doc ?pred powla:Document ;
  		dc:title ?title
} order by ?title
"""