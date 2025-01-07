WORDNET_RDF_HEADER = """
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix dc: <http://purl.org/dc/terms/> 
prefix ili: <http://globalwordnet.org/ili/> 
prefix lime: <http://www.w3.org/ns/lemon/lime#> 
prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> 
prefix owl: <http://www.w3.org/2002/07/owl#> 
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
prefix schema: <http://schema.org/> 
prefix skos: <http://www.w3.org/2004/02/skos/core#> 
prefix synsem: <http://www.w3.org/ns/lemon/synsem#> 
prefix wn: <https://globalwordnet.github.io/schemas/wn#> 
prefix wnlemma: <https://en-word.net/lemma/> 
prefix wnid: <https://en-word.net/id/>
"""

WORDNET_RDF_CNT_SELECT = """
SELECT (COUNT(*) AS ?count) FROM <https://passivlingo.com/graph/wordnet> 
"""

WORDNET_RDF_SELECT = """
SELECT ?lexEntry, ?canon, ?writtenRep, ?pos, ?sense, ?synset, ?def FROM <https://passivlingo.com/graph/wordnet> 
"""

WORDNET_RDF_SELECT_2 = """
SELECT ?synset, ?example FROM <https://passivlingo.com/graph/wordnet> 
"""

WORDNET_RDF_SELECT_3 = """
SELECT ?synset, ?def FROM <https://passivlingo.com/graph/wordnet> 
"""

WORDNET_RDF_SELECT_4 = """
SELECT ?lexEntry, ?writtenRep, ?pos FROM <https://passivlingo.com/graph/wordnet> 
"""

WORDNET_RDF_BODY_4 = """
where { 
?lexEntry a ontolex:LexicalEntry .
?lexEntry ontolex:canonicalForm ?canon .
?canon ontolex:writtenRep ?writtenRep .
?lexEntry wn:partOfSpeech ?pos .
FILTER(STRSTARTS(STR(?lexEntry), 'https://en-word.net'))
}
"""

WORDNET_RDF_BODY = """
where { 
?lexEntry a ontolex:LexicalEntry .
?lexEntry ontolex:canonicalForm ?canon .
?canon ontolex:writtenRep ?writtenRep .
?lexEntry wn:partOfSpeech ?pos .
?lexEntry ontolex:sense ?sense .
?sense ontolex:isLexicalizedSenseOf ?synset .
?synset wn:definition ?defRef .
?defRef rdf:value ?def .
}
"""
WORDNET_RDF_BODY_2 = """
where { 
?synset wn:example ?exampleRef .
?exampleRef rdf:value ?example .
}
"""

WORDNET_RDF_BODY_3 = """
where { 
?synset wn:definition ?defRef .
?defRef rdf:value ?def .
}
"""

RDF_FOOTER = """
LIMIT {LIMIT_VAR}
OFFSET {OFFSET_VAR}
"""

WORDNET_RDF = f'{WORDNET_RDF_HEADER}{WORDNET_RDF_SELECT}{WORDNET_RDF_BODY}{RDF_FOOTER}'
WORDNET_RDF_2 = f'{WORDNET_RDF_HEADER}{WORDNET_RDF_SELECT_2}{WORDNET_RDF_BODY_2}{RDF_FOOTER}'
WORDNET_RDF_3 = f'{WORDNET_RDF_HEADER}{WORDNET_RDF_SELECT_3}{WORDNET_RDF_BODY_3}{RDF_FOOTER}'
WORDNET_RDF_4 = f'{WORDNET_RDF_HEADER}{WORDNET_RDF_SELECT_4}{WORDNET_RDF_BODY_4}{RDF_FOOTER}'
WORDNET_RDF_CNT = f'{WORDNET_RDF_HEADER}{WORDNET_RDF_CNT_SELECT}{WORDNET_RDF_BODY}'


WIKTIONARY_DB_NOUNS_SMALL_CREATE = """
CREATE TABLE WIKT_NOUNS_SMALL_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL);
"""

WIKTIONARY_DB_CANON_FORM_CREATE = """
CREATE TABLE WIKT_CANON_FORM_STAGING
    (SUBJECT          TEXT    NOT NULL,
    CANON_FORM          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL,
    POS      TEXT     NOT NULL);
"""

WIKTIONARY_DB_NOUNS_SMALL_SELECT = """
SELECT DISTINCT SUBJECT, LABEL FROM WIKT_NOUNS_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT DISTINCT SUBJECT, LABEL FROM WIKT_NOUNS_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_NOUNS_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
);
"""

WIKTIONARY_DB_PROPER_NOUNS_SMALL_CREATE = """
CREATE TABLE WIKT_PROPER_NOUNS_SMALL_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL);
"""

WIKTIONARY_DB_PROPER_NOUNS_SMALL_SELECT = """
SELECT DISTINCT SUBJECT, LABEL FROM WIKT_PROPER_NOUNS_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT DISTINCT SUBJECT, LABEL FROM WIKT_PROPER_NOUNS_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_PROPER_NOUNS_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
);
"""

WIKTIONARY_DB_VERBS_SMALL_CREATE = """
CREATE TABLE WIKT_VERBS_SMALL_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL);
"""
WIKTIONARY_DB_VERBS_SMALL_SELECT = """
SELECT * FROM WIKT_VERBS_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT * FROM WIKT_VERBS_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_VERBS_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
)
"""

WIKTIONARY_DB_ADVERBS_SMALL_CREATE = """
CREATE TABLE WIKT_ADVERBS_SMALL_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL);
"""
WIKTIONARY_DB_ADVERBS_SMALL_SELECT = """
SELECT * FROM WIKT_ADVERBS_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT * FROM WIKT_ADVERBS_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_ADVERBS_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
);
"""

WIKTIONARY_DB_ADJECTIVES_SMALL_CREATE = """
CREATE TABLE WIKT_ADJECTIVES_SMALL_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL);
"""
WIKTIONARY_DB_ADJECTIVES_SMALL_SELECT = """
SELECT * FROM WIKT_ADJECTIVES_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT * FROM WIKT_ADJECTIVES_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_ADJECTIVES_SMALL_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
);
"""

WIKTIONARY_DB_CANON_FORM_SELECT = """
SELECT * FROM WIKT_CANON_FORM_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT * FROM WIKT_CANON_FORM_STAGING
WHERE SUBJECT NOT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
AND WRITTEN_REP NOT IN 
(
SELECT WRITTEN_REP FROM WIKT_CANON_FORM_STAGING
WHERE SUBJECT LIKE '%/eng/%'
AND SUBJECT LIKE '%__1%'
);
"""

WIKTIONARY_DB_NOUNS_SMALL_INSERT = """
INSERT INTO WIKT_NOUNS_SMALL_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP) VALUES (?, ?, ?)
"""

WIKTIONARY_DB_CANON_FORM_INSERT = """
INSERT INTO WIKT_CANON_FORM_STAGING 
(SUBJECT,
    CANON_FORM,         
    WRITTEN_REP,
    POS) VALUES (?, ?, ?, ?)
"""

WIKTIONARY_DB_PROPER_NOUNS_SMALL_INSERT = """
INSERT INTO WIKT_PROPER_NOUNS_SMALL_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP) VALUES (?, ?, ?)
"""

WIKTIONARY_DB_VERBS_SMALL_INSERT = """
INSERT INTO WIKT_VERBS_SMALL_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP) VALUES (?, ?, ?)
"""

WIKTIONARY_DB_ADVERBS_SMALL_INSERT = """
INSERT INTO WIKT_ADVERBS_SMALL_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP) VALUES (?, ?, ?)
"""

WIKTIONARY_DB_ADJECTIVES_SMALL_INSERT = """
INSERT INTO WIKT_ADJECTIVES_SMALL_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP) VALUES (?, ?, ?)
"""

WIKTIONARY_QUERY_HEADER = """
prefix dcterms:  <http://purl.org/dc/terms/> 
prefix deu:      <http://kaiko.getalp.org/dbnary/eng/> 
prefix lexinfo:  <http://www.lexinfo.net/ontology/2.0/lexinfo#> 
prefix lexvo:    <http://lexvo.org/id/iso639-3/> 
prefix olia:     <http://purl.org/olia/olia.owl#> 
prefix ontolex:  <http://www.w3.org/ns/lemon/ontolex#> 
prefix rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> 
"""

WIKTIONARY_CANON_FORM_SELECT = """
select distinct ?s ?label ?canonForm ?pos 
"""

WIKTIONARY_NOUNS_SELECT_SMALL = """
select distinct ?s ?label ?writtenRep 
"""

WIKTIONARY_OTHER_SELECT_SMALL = """
select distinct ?s ?label ?writtenRep
"""

WIKTIONARY_NOUNS_CNT_SELECT = """
SELECT (COUNT(*) AS ?count)
"""

WIKTIONARY_CANON_FORM_BODY = """
where { 
?s lexinfo:partOfSpeech ?pos .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:eng .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
}
"""

WIKTIONARY_NOUNS_BODY_SMALL = """
where { 
?s a lexinfo:Noun .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:eng .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""

WIKTIONARY_PROPER_NOUNS_BODY_SMALL = """
where { 
?s a lexinfo:ProperNoun .
?s dcterms:language  lexvo:eng .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""

WIKTIONARY_VERBS_BODY_SMALL = """
where { 
?s a lexinfo:Verb .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:eng .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""

WIKTIONARY_ADVERBS_BODY_SMALL = """
where { 
?s a lexinfo:Adverb .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:eng .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""

WIKTIONARY_ADJECTIVES_BODY_SMALL = """
where { 
?s a lexinfo:Adjective .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:eng .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""


WIKTIONARY_FOOTER = """
LIMIT {LIMIT_VAR}
OFFSET {OFFSET_VAR}
"""

WIKTIONARY_NOUNS_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_NOUNS_SELECT_SMALL}{WIKTIONARY_NOUNS_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_PROPER_NOUNS_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_NOUNS_SELECT_SMALL}{WIKTIONARY_PROPER_NOUNS_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_VERBS_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_OTHER_SELECT_SMALL}{WIKTIONARY_VERBS_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_ADVERBS_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_OTHER_SELECT_SMALL}{WIKTIONARY_ADVERBS_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_ADJECTIVES_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_OTHER_SELECT_SMALL}{WIKTIONARY_ADJECTIVES_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_CANON_FORM = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_CANON_FORM_SELECT}{WIKTIONARY_CANON_FORM_BODY}{WIKTIONARY_FOOTER}'

WIKTIONARY_NOUNS_CNT = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_NOUNS_CNT_SELECT}{WIKTIONARY_NOUNS_BODY_SMALL}'


WORDNET_RDF_SUBJECT_HASHED = WORDNET_RDF_HEADER + """
Select distinct * 
WHERE {
  ?subject ?predicate ?object .
  FILTER(STRSTARTS(STR(?subject), "https://en-word.net/") && CONTAINS(STR(?subject), "#"))  
}
""" + RDF_FOOTER

WORDNET_RDF_OBJECT_HASHED = WORDNET_RDF_HEADER + """
Select distinct * 
{
{
?subject ?predicate ?object .
FILTER(STRSTARTS(STR(?object), "https://en-word.net/") && CONTAINS(STR(?object), "#"))  
}
MINUS
{
Select distinct * 
WHERE {
  ?subject ?predicate ?object .
  FILTER(STRSTARTS(STR(?subject), "https://en-word.net/") && CONTAINS(STR(?subject), "#"))  
}
}
}
""" + RDF_FOOTER

SYNSET_NOUNS_STAGING_CREATE = """
CREATE TABLE SYNSET_NOUNS_STAGING
    (ID          TEXT    NOT NULL,
    ILI          TEXT    NOT NULL,         
    LEMMA      TEXT     NOT NULL,
    CONTENT_STR      TEXT     NOT NULL,
    DBPEDIA      TEXT     NOT NULL,
    CONFIDENCE      TEXT     NOT NULL,
    APPROVED      TEXT     NOT NULL);
"""

SYNSET_NOUNS_STAGING_KEA_INSERT = """
INSERT INTO SYNSET_NOUNS_STAGING_KEA 
(ID,
    ILI,         
    LEMMA,
    CONTENT_STR,
    DBPEDIA,
    CONFIDENCE,
    APPROVED) VALUES (?, ?, ?, ?, ?, ?, ?)
"""

SYNSET_NOUNS_STAGING_KEA_CREATE = """
CREATE TABLE SYNSET_NOUNS_STAGING_KEA
    (ID          TEXT    NOT NULL,
    ILI          TEXT    NOT NULL,         
    LEMMA      TEXT     NOT NULL,
    CONTENT_STR      TEXT     NOT NULL,
    DBPEDIA      TEXT     NOT NULL,
    CONFIDENCE      TEXT     NOT NULL,
    APPROVED      TEXT     NOT NULL);
"""

SYNSET_NOUNS_STAGING_INSERT = """
INSERT INTO SYNSET_NOUNS_STAGING 
(ID,
    ILI,         
    LEMMA,
    CONTENT_STR,
    DBPEDIA,
    CONFIDENCE,
    APPROVED) VALUES (?, ?, ?, ?, ?, ?, ?)
"""

SYNSET_NOUNS_STAGING_SELECT = """
SELECT t1.*
FROM SYNSET_NOUNS_STAGING t1
INNER JOIN (
    SELECT id, MAX(CAST(CONFIDENCE AS DECIMAL(10,6))) AS max_score
    FROM SYNSET_NOUNS_STAGING
    GROUP BY id
) t2 ON t1.id = t2.id AND CAST(t1.CONFIDENCE AS DECIMAL(10,6)) = t2.max_score AND t2.max_score > 0.98
order by CONFIDENCE
"""

SYNSET_NOUNS_STAGING_UPDATE = "UPDATE SYNSET_NOUNS_STAGING SET WIKIDATA = ? WHERE DBPEDIA = ?"
SYNSET_NOUNS_STAGING_KEA_UPDATE = "UPDATE SYNSET_NOUNS_STAGING_KEA SET WIKIDATA = ? WHERE DBPEDIA = ?"

GET_WIKIDATA_URI = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?wikidataUri
WHERE {
  <{DB_PEDIA_URI}> owl:sameAs ?wikidataUri .
  FILTER (STRSTARTS(str(?wikidataUri), "http://www.wikidata.org/entity/"))
}
"""

GET_WIKIDATA_CLASSES = """
SELECT *
WHERE
{
  <{WIKIDATA_URI}> (wdt:P31/wdt:P279) ?o  
}
"""

GET_WIKIDATA_MISMATCH = """
SELECT t1.id, t1.ILI, t1.LEMMA, t1.CONTENT_STR, t1.DBPEDIA, t1.WIKIDATA, t3.item
FROM SYNSET_NOUNS_STAGING t1
INNER JOIN (
    SELECT id, MAX(CAST(CONFIDENCE AS DECIMAL(10,6))) AS max_score
    FROM SYNSET_NOUNS_STAGING
    GROUP BY id
) t2 ON t1.id = t2.id AND CAST(t1.CONFIDENCE AS DECIMAL(10,6)) = t2.max_score AND t2.max_score > 0.98
inner join wikidata_ili as t3 on t1.ili = t3.id
where t1.WIKIDATA <> t3.item and t1.WIKIDATA <> 'http://www.wikidata.org/entity/Q10299641'
"""

GET_WIKIDATA_ALL_MISMATCH_ID = """
Select DISTINCT(wiki_id) FROM
(
SELECT t1.WIKIDATA as wiki_id
FROM SYNSET_NOUNS_STAGING t1
INNER JOIN (
    SELECT id, MAX(CAST(CONFIDENCE AS DECIMAL(10,6))) AS max_score
    FROM SYNSET_NOUNS_STAGING
    GROUP BY id
) t2 ON t1.id = t2.id AND CAST(t1.CONFIDENCE AS DECIMAL(10,6)) = t2.max_score AND t2.max_score > 0.98
inner join wikidata_ili as t3 on t1.ili = t3.id
where t1.WIKIDATA <> t3.item and t1.WIKIDATA <> 'http://www.wikidata.org/entity/Q10299641'
UNION
SELECT t3.item as wiki_id
FROM SYNSET_NOUNS_STAGING t1
INNER JOIN (
    SELECT id, MAX(CAST(CONFIDENCE AS DECIMAL(10,6))) AS max_score
    FROM SYNSET_NOUNS_STAGING
    GROUP BY id
) t2 ON t1.id = t2.id AND CAST(t1.CONFIDENCE AS DECIMAL(10,6)) = t2.max_score AND t2.max_score > 0.98
inner join wikidata_ili as t3 on t1.ili = t3.id
where t1.WIKIDATA <> t3.item and t1.WIKIDATA <> 'http://www.wikidata.org/entity/Q10299641'
)
"""
WIKIDATA_CLASSES_INSERT = """
INSERT INTO wikidata_classes
(wiki_entity,
    wiki_class) VALUES (?, ?)
"""


LOD_CLOSE_MATCHES = """
SELECT t1.ID, t1.ILI, t1.DBPEDIA, t1.WIKIDATA, t3.item
FROM SYNSET_NOUNS_STAGING t1
INNER JOIN (
    SELECT id, MAX(CAST(CONFIDENCE AS DECIMAL(10,6))) AS max_score
    FROM SYNSET_NOUNS_STAGING
    GROUP BY id
) t2 ON t1.id = t2.id AND CAST(t1.CONFIDENCE AS DECIMAL(10,6)) = t2.max_score AND t2.max_score > 0.98
left join wikidata_ili as t3 on t1.ili = t3.id
"""