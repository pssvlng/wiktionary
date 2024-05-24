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

INSERT_BFO = """
INSERT INTO BFO_STAGING
(ILI,
    BFO_CLASS,
    BFO_LABEL) VALUES (?, ?, ?)
"""

SELECT_MAX_BFO_CLASS = """
Select t4.ILI, t5.URI as BFO_CLASS, t5.DESCRIPTION, MAX(t5.LEVEL) as  MAX_LEVEL from BFO_STAGING t4
INNER JOIN BFO_CLASSES t5 on t4.BFO_CLASS = t5.URI
GROUP BY t4.ILI
HAVING MAX_LEVEL > 0
"""

SELECT_BFO_WORDNET_CLASSIFICATION = """
with f1 as (SELECT t1.ID, t1.ILI, t1.LEMMA, t1.CONTENT_STR, t1.DBPEDIA, t1.WIKIDATA
FROM SYNSET_NOUNS_STAGING t1
INNER JOIN (
    SELECT id, MAX(CAST(CONFIDENCE AS DECIMAL(10,6))) AS max_score
    FROM SYNSET_NOUNS_STAGING
    GROUP BY id
) t2 ON t1.id = t2.id AND CAST(t1.CONFIDENCE AS DECIMAL(10,6)) = t2.max_score AND t2.max_score > 0.98
),
f2 as (
Select t4.ILI, t5.URI as BFO_CLASS, t5.DESCRIPTION, MAX(t5.LEVEL) as  MAX_LEVEL from BFO_STAGING t4
INNER JOIN BFO_CLASSES t5 on t4.BFO_CLASS = t5.URI
GROUP BY t4.ILI
HAVING MAX_LEVEL > 0
)
select f1.ID, f1.ILI, f1.LEMMA, f1.CONTENT_STR, f1.DBPEDIA, f1.WIKIDATA, f2.BFO_CLASS, f2.DESCRIPTION from f1 
left join f2 on f2.ILI = f1.ILI
"""


