from SPARQLWrapper import JSON
from  SPARQLWrapper import SPARQLWrapper
import sqlite3
from queries_bfo import CREATE_BFO_TABLE, GET_BFO_CLASSES
from queries_en import LOD_CLOSE_MATCHES

def create_bfo_tables(dbName):    
    conn = sqlite3.connect(dbName)
    print(f"Opened {dbName} database successfully")
    conn.execute(CREATE_BFO_TABLE)    
    print("Table BFO_STAGING created successfully")    
    
    conn.close()

def get_bfo_classes(dbName):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()    
    rows = cursor.execute(LOD_CLOSE_MATCHES)
    data_to_insert = []
    cntr = 0
    for row in rows:
        wikidata_uri = str(row[3])
        wikidata_id = wikidata_uri[wikidata_uri.rfind('/'): len(wikidata_uri)]
        sparql_query = GET_BFO_CLASSES.replace("{WIKIDATA_ID}", wikidata_id)
        sparql = SPARQLWrapper("https://kaiko.getalp.org/sparql")    
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()    
            
        data_to_insert = [(result["item"]["value"],
                            result["itemLabel"]["value"])
                            for result in results["results"]["bindings"]]

        cntr += 1
        if cntr % 1000 == 0:
            print(f"Records processed: {cntr} of {len(rows)}")
    conn.close()

create_bfo_tables('synset_noun_en.db')    