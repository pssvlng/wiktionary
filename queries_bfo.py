BFO_ENDPOINT = "https://query.wikidata.org/"

GET_BFO_CLASSES = """
SELECT distinct ?item ?itemLabel 
WHERE
{    
  {
    wd:{WIKIDATA_ID} wdt:P31 ?item0 .    
    ?item0 wdt:P279* ?item .    
    ?item wdt:P31 wd:Q124711104 .
  }
  UNION {
    wd:{WIKIDATA_ID} wdt:P279* ?item .     
    ?item wdt:P31 wd:Q124711104 .
 }  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
}
"""

CREATE_BFO_TABLE = """
CREATE TABLE BFO_STAGING
    (ILI          TEXT    NOT NULL,
    BFO_CLASS          TEXT    NOT NULL,         
    BFO_LABEL      TEXT     NOT NULL);
"""
