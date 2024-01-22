import json
import sqlite3
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from rdflib import Namespace
import spacy

from queries import WIKTIONARY_DB_ADJECTIVES_SMALL_SELECT, WIKTIONARY_DB_ADVERBS_SMALL_SELECT, WIKTIONARY_DB_NOUNS_SMALL_SELECT, WIKTIONARY_DB_PROPER_NOUNS_SMALL_SELECT, WIKTIONARY_DB_VERBS_SMALL_SELECT

lexvo = {}
lexvo['en'] = 'http://www.lexvo.org/page/iso639-3/eng'
lexvo['de'] = 'http://www.lexvo.org/page/iso639-3/deu'

lexinfo_uri = 'http://www.lexinfo.net/ontology/2.0/lexinfo#'

spacy_to_olia = {}
spacy_to_olia['Nom'] = ('http://purl.org/olia/olia.owl#hasCase', 'http://purl.org/olia/olia.owl#Nominative')
spacy_to_olia['Acc'] = ('http://purl.org/olia/olia.owl#hasCase', 'http://purl.org/olia/olia.owl#Accusative ')
spacy_to_olia['Dat'] = ('http://purl.org/olia/olia.owl#hasCase', 'http://purl.org/olia/olia.owl#DativeCase')
spacy_to_olia['Gen'] = ('http://purl.org/olia/olia.owl#hasCase', 'http://purl.org/olia/olia.owl#GenitiveCase')

spacy_to_olia['1'] = ('http://purl.org/olia/olia.owl#hasNumber', 'http://purl.org/olia/olia.owl#First')
spacy_to_olia['2'] = ('http://purl.org/olia/olia.owl#hasNumber', 'http://purl.org/olia/olia.owl#Second')
spacy_to_olia['3'] = ('http://purl.org/olia/olia.owl#hasNumber', 'http://purl.org/olia/olia.owl#Third')

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

#spacy_to_olia['Fin'] = ('http://purl.org/olia/olia.owl#', 'http://purl.org/olia/olia.owl#')
#spacy_to_olia['Part'] = ('http://purl.org/olia/olia.owl#', 'http://purl.org/olia/olia.owl#')
spacy_to_olia['Inf'] = ('http://purl.org/olia/olia.owl#hasMood', 'http://purl.org/olia/olia.owl#Infinitive')

def get_noun_lookup_dict(db_name, query):
    result = {}
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        result[f'{row[1]}_{row[3]}'] = row[0]
    cursor.close()    
    conn.close()
    return result

def get_pos_lookup_dict(db_name, query):
    result = {}
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        result[f'{row[1]}_{row[2]}'] = row[0]
    cursor.close()    
    conn.close()
    return result

noun_lookup = get_noun_lookup_dict(WIKTIONARY_DB_NOUNS_SMALL_SELECT)
proper_noun_lookup = get_noun_lookup_dict(WIKTIONARY_DB_PROPER_NOUNS_SMALL_SELECT)
verb_lookup = get_pos_lookup_dict(WIKTIONARY_DB_VERBS_SMALL_SELECT)
adverb_lookup = get_pos_lookup_dict(WIKTIONARY_DB_ADVERBS_SMALL_SELECT)
adjective_lookup = get_pos_lookup_dict(WIKTIONARY_DB_ADJECTIVES_SMALL_SELECT)

nlp = {}
nlp['en'] = spacy.load('en_core_web_lg') 
nlp['de'] = spacy.load('de_core_news_lg')    

word_compare_lookup = {}
with open('de_0.json', "r") as json_file:
    word_compare_lookup['de_0'] = json.load(json_file)
with open('de_1.json', "r") as json_file:
    word_compare_lookup['de_1'] = json.load(json_file)      

nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
dbpedia = Namespace("http://dbpedia.org/resource/")
itsrdf = Namespace("http://www.w3.org/2005/11/its/rdf#")
curriculum_ns = Namespace("https://w3id.org/curriculum/")
ili_uri = "http://ili.globalwordnet.org/ili/"
ili_en_uri = "https://en-word.net/ttl/ili/"
olia_uri = "http://purl.org/olia/olia.owl#"
olia_ns = Namespace("http://purl.org/olia/olia.owl#")
oersi_ns = Namespace("https://edu.yovisto.com/resource/oersi#")

def remove_html_tags_and_whitespace(input_string):
    soup = BeautifulSoup(input_string, 'html.parser')        
    clean_string = soup.get_text()        
    clean_string = clean_string.strip()    
    return clean_string

def getSpacyToLexinfoPosMapping(pos):
        choices = {'VERB': 'verb', 'NOUN': 'noun',
                   'ADV': 'adverb', 'ADJ': 'adjective'}
        return choices.get(pos, 'x')

def getSpacyToWordnetPosMapping(pos):
        choices = {'VERB': 'v', 'NOUN': 'n',
                   'ADV': 'r', 'ADJ': 'a'}
        return choices.get(pos, 'x')

def tag_text(textToTag: str, lang = 'de'):
    def get_morph(token):
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
        words = nlp[lang](textToTag)                                                    
        for word in [ent for ent in words.ents]:                        
            entities.append((word.text, "NOUN", word.lemma_, "", True, get_morph(word)))
        
        for word in words:                        
            result.append((word.text, word.pos_, word.lemma_, word.whitespace_, False, get_morph(word)))
        
    except Exception as e:
        print(f'Spacy Tagger failed on following text: {textToTag}: {e}')        
    
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