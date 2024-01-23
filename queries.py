WIKTIONARY_DB_NOUNS_SMALL_CREATE = """
CREATE TABLE WIKT_NOUNS_SMALL_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL,
    GENDER            TEXT NOT NULL);
"""

WIKTIONARY_DB_NOUNS_SMALL_SELECT = """
SELECT DISTINCT SUBJECT, LABEL FROM WIKT_NOUNS_SMALL_STAGING
WHERE SUBJECT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT DISTINCT SUBJECT, LABEL FROM WIKT_NOUNS_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_NOUNS_SMALL_STAGING
WHERE SUBJECT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
);
"""

WIKTIONARY_DB_PROPER_NOUNS_SMALL_CREATE = """
CREATE TABLE WIKT_PROPER_NOUNS_SMALL_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL,
    GENDER            TEXT NOT NULL);
"""

WIKTIONARY_DB_PROPER_NOUNS_SMALL_SELECT = """
SELECT DISTINCT SUBJECT, LABEL FROM WIKT_PROPER_NOUNS_SMALL_STAGING
WHERE SUBJECT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT DISTINCT SUBJECT, LABEL FROM WIKT_PROPER_NOUNS_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_PROPER_NOUNS_SMALL_STAGING
WHERE SUBJECT LIKE '%/deu/%'
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
WHERE SUBJECT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT * FROM WIKT_VERBS_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_VERBS_SMALL_STAGING
WHERE SUBJECT LIKE '%/deu/%'
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
WHERE SUBJECT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT * FROM WIKT_ADVERBS_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_ADVERBS_SMALL_STAGING
WHERE SUBJECT LIKE '%/deu/%'
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
WHERE SUBJECT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
UNION
SELECT * FROM WIKT_ADJECTIVES_SMALL_STAGING
WHERE SUBJECT NOT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
AND LABEL NOT IN 
(
SELECT LABEL FROM WIKT_ADJECTIVES_SMALL_STAGING
WHERE SUBJECT LIKE '%/deu/%'
AND SUBJECT LIKE '%__1%'
);
"""

WIKTIONARY_DB_NOUNS_CREATE = """
CREATE TABLE WIKT_NOUNS_STAGING
    (SUBJECT          TEXT    NOT NULL,
    LABEL          TEXT    NOT NULL,         
    WRITTEN_REP      TEXT     NOT NULL,
    GENDER            TEXT NOT NULL,
    NOM_SINGL        TEXT       NOT NULL,
    NOM_SINGL_WRITTEN_REP TEXT       NOT NULL,
    NOM_PL        TEXT       NOT NULL,
    NOM_PL_WRITTEN_REP TEXT       NOT NULL,
    AKK_SINGL        TEXT       NOT NULL,
    AKK_SINGL_WRITTEN_REP TEXT       NOT NULL,
    AKK_PL        TEXT       NOT NULL,
    AKK_PL_WRITTEN_REP TEXT       NOT NULL,        
    DAT_SINGL        TEXT       NOT NULL,
    DAT_SINGL_WRITTEN_REP TEXT       NOT NULL,        
    DAT_PL        TEXT       NOT NULL,
    DAT_PL_WRITTEN_REP TEXT       NOT NULL,                
    GEN_SINGL        TEXT       NOT NULL,
    GEN_SINGL_WRITTEN_REP TEXT       NOT NULL,                
    GEN_PL        TEXT       NOT NULL,                                    
    GEN_PL_WRITTEN_REP TEXT       NOT NULL);
"""

WIKTIONARY_DB_NOUNS_INSERT = """
INSERT INTO WIKT_NOUNS_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP,
    GENDER,
    NOM_SINGL,
    NOM_SINGL_WRITTEN_REP,
    NOM_PL,
    NOM_PL_WRITTEN_REP,
    AKK_SINGL,
    AKK_SINGL_WRITTEN_REP,
    AKK_PL,
    AKK_PL_WRITTEN_REP,        
    DAT_SINGL,
    DAT_SINGL_WRITTEN_REP,        
    DAT_PL,
    DAT_PL_WRITTEN_REP,                
    GEN_SINGL,
    GEN_SINGL_WRITTEN_REP,                
    GEN_PL,                                    
    GEN_PL_WRITTEN_REP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

WIKTIONARY_DB_NOUNS_SMALL_INSERT = """
INSERT INTO WIKT_NOUNS_SMALL_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP,
    GENDER) VALUES (?, ?, ?, ?)
"""

WIKTIONARY_DB_PROPER_NOUNS_SMALL_INSERT = """
INSERT INTO WIKT_PROPER_NOUNS_SMALL_STAGING 
(SUBJECT,
    LABEL,         
    WRITTEN_REP,
    GENDER) VALUES (?, ?, ?, ?)
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
prefix deu:      <http://kaiko.getalp.org/dbnary/deu/> 
prefix lexinfo:  <http://www.lexinfo.net/ontology/2.0/lexinfo#> 
prefix lexvo:    <http://lexvo.org/id/iso639-3/> 
prefix olia:     <http://purl.org/olia/olia.owl#> 
prefix ontolex:  <http://www.w3.org/ns/lemon/ontolex#> 
prefix rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> 
"""

WIKTIONARY_NOUNS_SELECT = """
select distinct ?s ?label ?writtenRep ?gender 
?otherFormNomSingular ?nomWrittenRepSingular ?otherFormNomPlural  ?nomWrittenRepPlural
?otherFormAkkSingular ?akkWrittenRepSingular ?otherFormAkkPlural  ?akkWrittenRepPlural
?otherFormDatSingular ?datWrittenRepSingular ?otherFormDatPlural  ?datWrittenRepPlural
?otherFormGenSingular ?genWrittenRepSingular ?otherFormGenPlural  ?genWrittenRepPlural
"""

WIKTIONARY_NOUNS_SELECT_SMALL = """
select distinct ?s ?label ?writtenRep ?gender 
"""

WIKTIONARY_OTHER_SELECT_SMALL = """
select distinct ?s ?label ?writtenRep
"""

WIKTIONARY_NOUNS_CNT_SELECT = """
SELECT (COUNT(*) AS ?count)
"""
WIKTIONARY_NOUNS_BODY = """
where { 
?s a lexinfo:Noun .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:deu .
?s lexinfo:gender ?gender.
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .

?s ontolex:otherForm ?otherFormNomSingular .
?otherFormNomSingular olia:hasCase olia:Nominative .
?otherFormNomSingular olia:hasNumber olia:Singular .
?otherFormNomSingular ontolex:writtenRep ?nomWrittenRepSingular .

?s ontolex:otherForm ?otherFormNomPlural .
?otherFormNomPlural olia:hasCase olia:Nominative .
?otherFormNomPlural olia:hasNumber olia:Plural .
?otherFormNomPlural ontolex:writtenRep ?nomWrittenRepPlural .

?s ontolex:otherForm ?otherFormAkkSingular .
?otherFormAkkSingular olia:hasCase olia:Accusative .
?otherFormAkkSingular olia:hasNumber olia:Singular .
?otherFormAkkSingular ontolex:writtenRep ?akkWrittenRepSingular .

?s ontolex:otherForm ?otherFormAkkPlural .
?otherFormAkkPlural olia:hasCase olia:Accusative .
?otherFormAkkPlural olia:hasNumber olia:Plural .
?otherFormAkkPlural ontolex:writtenRep ?akkWrittenRepPlural .

?s ontolex:otherForm ?otherFormDatSingular .
?otherFormDatSingular olia:hasCase olia:DativeCase .
?otherFormDatSingular olia:hasNumber olia:Singular .
?otherFormDatSingular ontolex:writtenRep ?datWrittenRepSingular .

?s ontolex:otherForm ?otherFormDatPlural .
?otherFormDatPlural olia:hasCase olia:DativeCase .
?otherFormDatPlural olia:hasNumber olia:Plural .
?otherFormDatPlural ontolex:writtenRep ?datWrittenRepPlural .

?s ontolex:otherForm ?otherFormGenSingular .
?otherFormGenSingular olia:hasCase olia:GenitiveCase .
?otherFormGenSingular olia:hasNumber olia:Singular .
?otherFormGenSingular ontolex:writtenRep ?genWrittenRepSingular .

?s ontolex:otherForm ?otherFormGenPlural .
?otherFormGenPlural olia:hasCase olia:GenitiveCase .
?otherFormGenPlural olia:hasNumber olia:Plural .
?otherFormGenPlural ontolex:writtenRep ?genWrittenRepPlural .

}
"""
WIKTIONARY_NOUNS_BODY_SMALL = """
where { 
?s a lexinfo:Noun .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:deu .
?s lexinfo:gender ?gender.
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""

WIKTIONARY_PROPER_NOUNS_BODY_SMALL = """
where { 
?s a lexinfo:ProperNoun .
?s dcterms:language  lexvo:deu .
?s lexinfo:gender ?gender.
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""

WIKTIONARY_VERBS_BODY_SMALL = """
where { 
?s a lexinfo:Verb .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:deu .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""

WIKTIONARY_ADVERBS_BODY_SMALL = """
where { 
?s a lexinfo:Adverb .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:deu .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""

WIKTIONARY_ADJECTIVES_BODY_SMALL = """
where { 
?s a lexinfo:Adjective .
?s a ontolex:LexicalEntry .
?s dcterms:language  lexvo:deu .
?s rdfs:label ?label .
?s ontolex:canonicalForm ?canonForm .
?canonForm ontolex:writtenRep ?writtenRep .
}
"""


WIKTIONARY_FOOTER = """
LIMIT {LIMIT_VAR}
OFFSET {OFFSET_VAR}
"""

WIKTIONARY_NOUNS = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_NOUNS_SELECT}{WIKTIONARY_NOUNS_BODY}{WIKTIONARY_FOOTER}'

WIKTIONARY_NOUNS_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_NOUNS_SELECT_SMALL}{WIKTIONARY_NOUNS_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_PROPER_NOUNS_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_NOUNS_SELECT_SMALL}{WIKTIONARY_PROPER_NOUNS_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_VERBS_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_OTHER_SELECT_SMALL}{WIKTIONARY_VERBS_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_ADVERBS_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_OTHER_SELECT_SMALL}{WIKTIONARY_ADVERBS_BODY_SMALL}{WIKTIONARY_FOOTER}'
WIKTIONARY_ADJECTIVES_SMALL = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_OTHER_SELECT_SMALL}{WIKTIONARY_ADJECTIVES_BODY_SMALL}{WIKTIONARY_FOOTER}'

WIKTIONARY_NOUNS_CNT = f'{WIKTIONARY_QUERY_HEADER}{WIKTIONARY_NOUNS_CNT_SELECT}{WIKTIONARY_NOUNS_BODY}'