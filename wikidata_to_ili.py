import sqlite3
from rdflib import Graph, URIRef, Literal

db_name = f"synset_noun_en.db"
conn = sqlite3.connect(db_name)    
cursor = conn.cursor()
cursor.execute("select * from wikidata_ili")
rows = cursor.fetchall()    
cntr = 0
graph = Graph()
for row in rows:    
    graph.add((URIRef(row[0]), URIRef('https://edu.yovisto.com/ontology/ili'), URIRef(f'http://globalwordnet.org/ili/{row[1]}')))

output_file = "wikidata_to_ili.ttl"
graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')            
conn.close()