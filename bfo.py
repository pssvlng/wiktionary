import time
from SPARQLWrapper import JSON
from  SPARQLWrapper import SPARQLWrapper
import sqlite3
from queries_bfo import CREATE_BFO_TABLE, GET_BFO_CLASSES, INSERT_BFO
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
    cursor.execute(LOD_CLOSE_MATCHES)
    rows = cursor.fetchall()    
    data_to_insert = []
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")                    
    cntr = 45000
    for row in rows[45000:]:
        wikidata_uri = str(row[3])
        wikidata_id = wikidata_uri[wikidata_uri.rfind('/') + 1: len(wikidata_uri)]
        sparql_query = GET_BFO_CLASSES.replace("{WIKIDATA_ID}", wikidata_id)        
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        try:
            results = sparql.query().convert()    
        except:
            time.sleep(30)    
            print(f"Timeout on: {cntr} of {len(rows)}. Trying again ...")
            results = sparql.query().convert()    

        data_to_insert.extend([(str(row[1]),
                            result["item"]["value"],
                            result["itemLabel"]["value"])
                            for result in results["results"]["bindings"]])

        cntr += 1
        if cntr % 100 == 0:
            cursor.executemany(INSERT_BFO, data_to_insert)            
            conn.commit()
            data_to_insert.clear()
            time.sleep(5)
            print(f"Records processed: {cntr} of {len(rows)}")

    cursor.executemany(INSERT_BFO, data_to_insert)            
    conn.commit()
    conn.close()

#create_bfo_tables('synset_noun_en.db')    
get_bfo_classes('synset_noun_en.db')    