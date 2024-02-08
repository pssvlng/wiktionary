

import os
import sqlite3

from SPARQLWrapper import JSON
from  SPARQLWrapper import SPARQLWrapper

from queries_en import WIKTIONARY_ADJECTIVES_SMALL, WIKTIONARY_ADVERBS_SMALL, WIKTIONARY_DB_ADJECTIVES_SMALL_CREATE, WIKTIONARY_DB_ADJECTIVES_SMALL_INSERT, WIKTIONARY_DB_ADVERBS_SMALL_CREATE, WIKTIONARY_DB_ADVERBS_SMALL_INSERT, WIKTIONARY_DB_NOUNS_SMALL_CREATE, WIKTIONARY_DB_NOUNS_SMALL_INSERT, WIKTIONARY_DB_PROPER_NOUNS_SMALL_CREATE, WIKTIONARY_DB_PROPER_NOUNS_SMALL_INSERT, WIKTIONARY_DB_VERBS_SMALL_CREATE, WIKTIONARY_DB_VERBS_SMALL_INSERT, WIKTIONARY_NOUNS_CNT, WIKTIONARY_NOUNS_SMALL, WIKTIONARY_PROPER_NOUNS_SMALL, WIKTIONARY_VERBS_SMALL

def createWiktionaryDB(dbName):
    #if os.path.isfile(dbName):
    #   return

    conn = sqlite3.connect(dbName)
    print(f"Opened {dbName} database successfully")
    conn.execute(WIKTIONARY_DB_PROPER_NOUNS_SMALL_CREATE)    
    print("Table WIKT_PROPER_NOUNS_STAGING created successfully")    
    # conn.execute(WIKTIONARY_DB_NOUNS_CREATE)    
    # print("Table WIKT__NOUNS_STAGING created successfully")    
    # conn.execute(WIKTIONARY_DB_VERBS_SMALL_CREATE)    
    # print("Table WIKT_VERBS_STAGING created successfully")    
    # conn.execute(WIKTIONARY_DB_ADVERBS_SMALL_CREATE)    
    # print("Table WIKT_ADVERBS_STAGING created successfully")    
    # conn.execute(WIKTIONARY_DB_ADJECTIVES_SMALL_CREATE)    
    # print("Table WIKT_ADJECTIVES_STAGING created successfully")    
    # conn.close()

def get_wiktionary_cnt(query):
    sparql = SPARQLWrapper("https://kaiko.getalp.org/sparql")        
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    print(f"Wiktionary Nouns Record Count: {results[0]['count']['value']}")

def get_wiktionary_other_small(limit: int, offset: int, db_name:str, get_query:str, insert_query:str):    
    sparql = SPARQLWrapper("https://kaiko.getalp.org/sparql")    
    get_query = get_query.replace('{LIMIT_VAR}', str(limit))
    get_query = get_query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(get_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    
    cntr = 0
    data_to_insert = [(result["s"]["value"],
                        result["label"]["value"], 
                        result["writtenRep"]["value"])
                        for result in results["results"]["bindings"]]
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()
    conn.close()

def get_wiktionary_proper_nouns_small(limit: int, offset: int, db_name:str, get_query:str, insert_query:str):    
    sparql = SPARQLWrapper("https://kaiko.getalp.org/sparql")    
    get_query = get_query.replace('{LIMIT_VAR}', str(limit))
    get_query = get_query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(get_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    
    cntr = 0
    data_to_insert = [(result["s"]["value"],
                        result["label"]["value"], 
                        result["writtenRep"]["value"])
                        for result in results["results"]["bindings"]]
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()
    conn.close()

def get_wiktionary_nouns_small(limit: int, offset: int, db_name:str):    
    sparql = SPARQLWrapper("https://kaiko.getalp.org/sparql")
    query = WIKTIONARY_NOUNS_SMALL    
    query = query.replace('{LIMIT_VAR}', str(limit))
    query = query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    
    cntr = 0
    data_to_insert = [(result["s"]["value"],
                        result["label"]["value"], 
                        result["writtenRep"]["value"])
                        for result in results["results"]["bindings"]]
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany(WIKTIONARY_DB_NOUNS_SMALL_INSERT, data_to_insert)
    conn.commit()
    conn.close()

   
#Main Program
#get_wiktionary_cnt(WIKTIONARY_NOUNS_CNT)
db_name = "wiktionary_en.db"
createWiktionaryDB(db_name)    

# for x in range(0,12):    
#    offset = 10000 * x
#    get_wiktionary_nouns_small(10000, offset, db_name)

for x in range(0,12):    
   offset = 10000 * x
   get_wiktionary_proper_nouns_small(10000, offset, db_name, WIKTIONARY_PROPER_NOUNS_SMALL, WIKTIONARY_DB_PROPER_NOUNS_SMALL_INSERT)

# for x in range(0,8):    
#    offset = 10000 * x
#    get_wiktionary_other_small(10000, offset, db_name, WIKTIONARY_VERBS_SMALL, WIKTIONARY_DB_VERBS_SMALL_INSERT)    

# for x in range(0,14):    
#     offset = 10000 * x
#     get_wiktionary_other_small(10000, offset, db_name, WIKTIONARY_ADJECTIVES_SMALL, WIKTIONARY_DB_ADJECTIVES_SMALL_INSERT)    

# for x in range(0,1):    
#     offset = 10000 * x
#     get_wiktionary_other_small(10000, offset, db_name, WIKTIONARY_ADVERBS_SMALL, WIKTIONARY_DB_ADVERBS_SMALL_INSERT)    