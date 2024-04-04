BFO_ENDPOINT = "https://query.wikidata.org/"

GET_BFO_CLASSES = """
SELECT distinct ?item ?itemLabel 
WHERE
{    
  {
    {WIKIDATA_URI} wdt:P31 ?item0 .    
    ?item0 wdt:P279* ?item .    
    ?item wdt:P31 wd:Q124711104 .
  }
  UNION {
    {WIKIDATA_URI} wdt:P279* ?item .     
    ?item wdt:P31 wd:Q124711104 .
 }  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
}
"""