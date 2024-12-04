import json
import sqlite3
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from rdflib import Namespace
import spacy
from spacy.tokens import MorphAnalysis
from collections import defaultdict
#from queries import WIKTIONARY_DB_ADJECTIVES_SMALL_SELECT, WIKTIONARY_DB_ADVERBS_SMALL_SELECT, WIKTIONARY_DB_NOUNS_SMALL_SELECT, WIKTIONARY_DB_PROPER_NOUNS_SMALL_SELECT, WIKTIONARY_DB_VERBS_SMALL_SELECT
import queries
import queries_en
from polyglot.text import Text

lexvo = {}
lexvo['en'] = 'http://www.lexvo.org/page/iso639-3/eng'
lexvo['de'] = 'http://www.lexvo.org/page/iso639-3/deu'

lexinfo_uri = 'http://www.lexinfo.net/ontology/2.0/lexinfo#'

spacy_to_olia = defaultdict(lambda: None)
spacy_to_olia['Nom'] = ('http://purl.org/olia/olia.owl#hasCase', 'http://purl.org/olia/olia.owl#Nominative')
spacy_to_olia['Acc'] = ('http://purl.org/olia/olia.owl#hasCase', 'http://purl.org/olia/olia.owl#Accusative')
spacy_to_olia['Dat'] = ('http://purl.org/olia/olia.owl#hasCase', 'http://purl.org/olia/olia.owl#DativeCase')
spacy_to_olia['Gen'] = ('http://purl.org/olia/olia.owl#hasCase', 'http://purl.org/olia/olia.owl#GenitiveCase')

spacy_to_olia['1'] = ('http://purl.org/olia/olia.owl#hasPerson', 'http://purl.org/olia/olia.owl#First')
spacy_to_olia['2'] = ('http://purl.org/olia/olia.owl#hasPerson', 'http://purl.org/olia/olia.owl#Second')
spacy_to_olia['3'] = ('http://purl.org/olia/olia.owl#hasPerson', 'http://purl.org/olia/olia.owl#Third')

spacy_to_olia['Fem'] = ('http://www.lexinfo.net/ontology/2.0/lexinfo#gender', 'http://www.lexinfo.net/ontology/2.0/lexinfo#feminine')
spacy_to_olia['Masc'] = ('http://www.lexinfo.net/ontology/2.0/lexinfo#gender', 'http://www.lexinfo.net/ontology/2.0/lexinfo#masculine')
spacy_to_olia['Neut'] = ('http://www.lexinfo.net/ontology/2.0/lexinfo#gender', 'http://www.lexinfo.net/ontology/2.0/lexinfo#neuter')

spacy_to_olia['Plur'] = ('http://purl.org/olia/olia.owl#hasNumber', 'http://purl.org/olia/olia.owl#Plural')
spacy_to_olia['Sing'] = ('http://purl.org/olia/olia.owl#hasNumber', 'http://purl.org/olia/olia.owl#Singular')

spacy_to_olia['Ind'] = ('http://purl.org/olia/olia.owl#hasMood', 'http://purl.org/olia/olia.owl#IndicativeMood')
spacy_to_olia['Sub'] = ('http://purl.org/olia/olia.owl#hasMood', 'http://purl.org/olia/olia.owl#SubjunctiveMood')
spacy_to_olia['Imp'] = ('http://purl.org/olia/olia.owl#hasMood', 'http://purl.org/olia/olia.owl#ImperativeMood')

spacy_to_olia['Pres'] = ('http://purl.org/olia/olia.owl#hasTense', 'http://purl.org/olia/olia.owl#Present')
spacy_to_olia['Past'] = ('http://purl.org/olia/olia.owl#hasTense', 'http://purl.org/olia/olia.owl#Past')

spacy_to_olia['Pos'] = ('http://purl.org/olia/olia.owl#hasDegree', 'http://purl.org/olia/olia.owl#Positive')
spacy_to_olia['Sup'] = ('http://purl.org/olia/olia.owl#hasDegree', 'http://purl.org/olia/olia.owl#Superlative')
spacy_to_olia['Cmp'] = ('http://purl.org/olia/olia.owl#hasDegree', 'http://purl.org/olia/olia.owl#Comparative')

#spacy_to_olia['Fin'] = ('http://purl.org/olia/olia.owl#', 'http://purl.org/olia/olia.owl#')
#spacy_to_olia['Part'] = ('http://purl.org/olia/olia.owl#', 'http://purl.org/olia/olia.owl#')
spacy_to_olia['Inf'] = ('http://purl.org/olia/olia.owl#hasMood', 'http://purl.org/olia/olia.owl#Infinitive')

def get_pos_lookup_dict(db_name, query):
    result = defaultdict(lambda: None)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        result[f'{row[1].upper()}'] = row[0]
    cursor.close()    
    conn.close()
    return result

def get_canon_lookup_dict(db_name, query):
    result = defaultdict(lambda: None)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        result[f'{row[0].upper()}'] = row[1]
    cursor.close()    
    conn.close()
    return result    

def get_dbnary_uri_prop_noun(lemma, lang = 'de'):
    proper_noun_lookup[lang][lemma.upper()]

def get_dbnary_uri_canon(subject, lang = 'en'):
    return canon_lookup[lang][subject]

def get_dbnary_uri(lemma, pos, lang = 'de'):
    if pos == 'verb':
        return verb_lookup[lang][lemma.upper()]
    if pos == 'noun':
        return noun_lookup[lang][lemma.upper()]
    if pos == 'adverb':
        return adverb_lookup[lang][lemma.upper()]
    if pos == 'adjective':
        return adjective_lookup[lang][lemma.upper()]
    raise Exception("Unknown pos: ", pos)

db_name = {}
db_name['de'] = 'wiktionary.db'
db_name['en'] = 'wiktionary_en.db'

canon_lookup = {}
canon_lookup['en'] = get_canon_lookup_dict(db_name['en'], queries_en.WIKTIONARY_DB_CANON_FORM_SELECT)

noun_lookup = {}
noun_lookup['de'] = get_pos_lookup_dict(db_name['de'], queries.WIKTIONARY_DB_NOUNS_SMALL_SELECT)
noun_lookup['en'] = get_pos_lookup_dict(db_name['en'], queries_en.WIKTIONARY_DB_NOUNS_SMALL_SELECT)
proper_noun_lookup = {}
proper_noun_lookup['de'] = get_pos_lookup_dict(db_name['de'], queries.WIKTIONARY_DB_PROPER_NOUNS_SMALL_SELECT)
proper_noun_lookup['en'] = get_pos_lookup_dict(db_name['en'], queries_en.WIKTIONARY_DB_PROPER_NOUNS_SMALL_SELECT)
verb_lookup = {}
verb_lookup['de'] = get_pos_lookup_dict(db_name['de'], queries.WIKTIONARY_DB_VERBS_SMALL_SELECT)
verb_lookup['en'] = get_pos_lookup_dict(db_name['en'], queries_en.WIKTIONARY_DB_VERBS_SMALL_SELECT)
adverb_lookup = {}
adverb_lookup['de'] = get_pos_lookup_dict(db_name['de'], queries.WIKTIONARY_DB_ADVERBS_SMALL_SELECT)
adverb_lookup['en'] = get_pos_lookup_dict(db_name['en'], queries_en.WIKTIONARY_DB_ADVERBS_SMALL_SELECT)
adjective_lookup = {}
adjective_lookup['de'] = get_pos_lookup_dict(db_name['de'], queries.WIKTIONARY_DB_ADJECTIVES_SMALL_SELECT)
adjective_lookup['en'] = get_pos_lookup_dict(db_name['en'], queries_en.WIKTIONARY_DB_ADJECTIVES_SMALL_SELECT)

nlp = {}
nlp['en'] = spacy.load('en_core_web_lg') 
nlp['de'] = spacy.load('de_core_news_lg')

spotlight_url = {}
spotlight_url['de'] = 'https://wlo.yovisto.com/spotlight/annotate'
spotlight_url['en'] = 'http://localhost:2222/rest/annotate'

word_compare_lookup = {}
with open('de_0.json', "r") as json_file:
    word_compare_lookup['de_0'] = json.load(json_file)
with open('de_1.json', "r") as json_file:
    word_compare_lookup['de_1'] = json.load(json_file)      
with open('en_0.json', "r") as json_file:
    word_compare_lookup['en_0'] = json.load(json_file)
with open('en_1.json', "r") as json_file:
    word_compare_lookup['en_1'] = json.load(json_file)          

nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
dbpedia = Namespace("http://dbpedia.org/resource/")
itsrdf = Namespace("http://www.w3.org/2005/11/its/rdf#")
curriculum_ns = Namespace("https://w3id.org/curriculum/")
ili_uri = "http://globalwordnet.org/ili/"
ili_en_uri = "https://en-word.net/ili/"
olia_uri = "http://purl.org/olia/olia.owl#"
olia_ns = Namespace("http://purl.org/olia/olia.owl#")
oersi_ns = Namespace("https://edu.yovisto.com/resource/oersi#")
wn_ns = Namespace("https://globalwordnet.github.io/schemas/wn#")

def remove_html_tags_and_whitespace(input_string):
    soup = BeautifulSoup(input_string, 'html.parser')        
    clean_string = soup.get_text()        
    clean_string = clean_string.strip()    
    return clean_string

def getSpacyToOliaPosMapping(pos):
        choices = {'VERB': 'verb', 'NOUN': 'noun',
                   'ADV': 'adverb', 'ADJ': 'adjective'}
        return choices.get(pos, 'x')

def getSpacyToWordnetPosMapping(pos):
        choices = {'VERB': 'v', 'NOUN': 'n',
                   'ADV': 'r', 'ADJ': 'a'}
        return choices.get(pos, 'x')

def tag_text(textToTag: str, lang = 'de'):
    def get_morph(token):
        if not hasattr(token, 'morph'):        
            return []
        morph_analysis = list(filter(lambda x: len(x) == 1, 
            [token.morph.get("Case", None),
            token.morph.get("Gender", None), 
            token.morph.get("Number", None),
            token.morph.get("Degree", None),
            token.morph.get("Person", None),
            token.morph.get("VerbForm", None),
            token.morph.get("Mood", None),
            token.morph.get("Tense", None)        
        ]))    
        return [x[0] for x in morph_analysis]
    
    result = []
    entities = []
    if not textToTag:
        return (result, entities)    
        
    try:        
        #doc =  Text(textToTag, hint_language_code='de')
        #for entity in doc.entities:
        #    entities.append((' '.join(entity), "NOUN", ' '.join(entity), "", True, []))
            
        words = nlp[lang](textToTag)                                                    
        #for word in [ent for ent in words.ents]:                        
        #for ent in words.ents:                            
        #    if ent.label_ in ["PERSON", "ORG", "GPE"]:
        #        entities.append((ent.text, "NOUN", ent.lemma_, "", True, get_morph(ent)))
        
        for word in words:                        
            #if word.pos_ == "PROPN":
            #    entities.append((word.text, "NOUN", word.lemma_, "", True, get_morph(word)))             
            result.append((word.text, word.pos_, word.lemma_, word.whitespace_, False, get_morph(word)))
        
    except Exception as e:
        print(f'Named Entity Tagger failed on following text: {textToTag}: {e}')        
    
    return (result, entities)    

def merge_lists(entities, words):
    last_index = 0
    for entry in entities:
        to_search = entry[0].split(' ')
        search_surface = [word[0] for word in words[last_index:]]
        for index, _ in enumerate(search_surface):
            if entry[0] == ' '.join(search_surface[index:index + len(to_search)]):                    
                try:
                    last_index += index
                    whitespace = words[last_index + len(to_search) - 1][3]
                    words[last_index:last_index + len(to_search) - 1] = []
                    if last_index >= len(words):
                        words.append((entry[0], entry[1], entry[2], whitespace, entry[4], entry[5]))
                    else:   
                        words[last_index] = (entry[0], entry[1], entry[2], whitespace, entry[4], entry[5])                    
                    last_index += 1
                    break
                except Exception as e:
                    print(f"Error while processing Named Entities in Generic Tokenizer: {e}")
                    
    return words

def add_unique_triple(g, subject, predicate, object):
    if (subject, predicate, object) not in g:
        g.add((subject, predicate, object))
    return g    