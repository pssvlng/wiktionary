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
WORDNET_RDF_CNT = f'{WORDNET_RDF_HEADER}{WORDNET_RDF_CNT_SELECT}{WORDNET_RDF_BODY}'


WIKTIONARY_DB_NOUNS_SMALL_CREATE = """
CREATE TABLE WIKT_NOUNS_SMALL_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL);
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

WIKTIONARY_DB_NOUNS_SMALL_INSERT = """
INSERT INTO WIKT_NOUNS_SMALL_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP) VALUES (?, ?, ?)
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

WIKTIONARY_NOUNS_SELECT_SMALL = """
select distinct ?s ?label ?writtenRep 
"""

WIKTIONARY_OTHER_SELECT_SMALL = """
select distinct ?s ?label ?writtenRep
"""

WIKTIONARY_NOUNS_CNT_SELECT = """
SELECT (COUNT(*) AS ?count)
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

WIKTIONARY_NOUNS_CNT = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_NOUNS_CNT_SELECT}{WIKTIONARY_NOUNS_BODY_SMALL}'