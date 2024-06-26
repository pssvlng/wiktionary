import os
import spacy
import nltk
#from nltk.corpus import tiger
from rdflib import Graph
from spacy.tokens import MorphAnalysis
from polyglot.text import Text

from rdflib import Graph

from shared import spacy_to_olia
import requests
import json

def batched_parse(graph, file_path, batch_size=1000):
    with open(file_path, 'rb') as file:
        for i, line in enumerate(file):
            graph.parse(data=line, format='nt')
            if i % batch_size == 0:                
                process_batch(graph)
                graph.remove((None, None, None))

def process_batch(graph):
    grouped_by_subject = {}
    for subj, pred, obj in graph:
        if subj not in grouped_by_subject:
            grouped_by_subject[subj] = []
        grouped_by_subject[subj].append((subj, pred, obj))

    for subject, triples in grouped_by_subject.items():
        print(f"Subject: {subject}")
        for triple in triples:
            print(f"  Triple: {triple}")
        print("=" * 40)

def func2(doc):
    for token in doc:
            print(
                f"{token.text}({token.lemma_}) - {token.pos_} - {token.dep_}: {str(token.morph)}"
            )
def get_verb_triples(token):
    result = {}
    result["Mood"] = token.morph.get("Moode", None)
    result["Person"] = token.morph.get("Person", None)
    result["Tense"] = token.morph.get("Temse", None)    

    
def get_adverb_triples(token):
    pass
def get_adjective_triples(token):
    pass
def get_noun_triples(token):
    result = {}
    result["Case"] = token.morph.get("Case", None)
    result["Gender"] = token.morph.get("Gender", None)
    result["Number"] = token.morph.get("Number", None)
    result["Degree"] = token.morph.get("Degree", None)

    

def get_triples(doc):
    result = []
    
    for token in doc:
        morph_analysis = list(filter(lambda x: x is not None, 
            [token.morph.get("Case", None),
            token.morph.get("Gender", None), 
            token.morph.get("Number", None),
            token.morph.get("Degree", None),
            token.morph.get("Person", None),
            token.morph.get("VerbForm", None),
            token.morph.get("Mood", None),
            token.morph.get("Tense", None)        
        ]))        
         
        if token.pos_ in ["VERB", "AUX", "ADV", "NOUN", "ADJ"]:
            for value in morph_analysis:
                if value in spacy_to_olia:
                    pred_obj = spacy_to_olia[value]

        
    return result        

    
def evaluate_description(description):
    nlp = spacy.load("de_core_news_sm")    
    words = nlp(description)
    if len(words) < 5:
        return (2, "Beschreibung zu kurz")
    
    nouns_and_named_entities = [token.text for token in words if token.pos_ == "NOUN" or token.ent_type_ != ""]
    if len(nouns_and_named_entities) == 0:
        return (2, "mindestens ein Substantiv im Beschreibungstext erforderlich")
    
    verbs = [token.text for token in words if token.pos_ in ["VERB", "AUX"]]
    if len(verbs) == 0:
        return (1, "Der Text enthält keine Verben")

    return (0, "")



def evaluate_description_http(description, lang):

    url = 'http://127.0.0.1:5000/api/validate/description'
    params = {
        'text': description,
        'lang': lang
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(params)
    response = requests.post(url, data=json_data, headers=headers)
    print(response)

#graph = Graph()
#ttl_file_path = f'{os.path.expanduser("~")}/MyData/dbnary/de_dbnary_morphology.ttl'
#batched_parse(graph, ttl_file_path)

# with open('file1.txt', 'r', encoding='utf-8') as file:    
#    file_content = file.readlines()

#nltk.download()
#sentences = tiger.sents()
#nlp = spacy.load("de_core_news_sm")
#m = MorphAnalysis(nlp.vocab)
#print(m.get('VerbForm'))

# print(" ".join(file_content))
# sentence_str = " ".join(file_content)
#sentence_str = "mir wird es von ihm fliessend gesagt."
#sentence_str2 = "die schönste Interpretationen von schönen Nachrichten diskutieren"
#doc = nlp(sentence_str2)
#func2(doc)

# txt =  """
# Ich wohne in Berlin, and ich arbeite für Apple. Ich liebe Kapstadt, und ich besuche Donald Trump in Berlin.
# """
# doc =  Text(txt, hint_language_code='de')
# 
# for entity in doc.entities:
    # print(' '.join(entity))

#for ent in doc.ents:
#    print(ent.text, ent.label_)

description_good = "Das hier ist ein gültiges Text."
description_bad1 = "zu kurz"
description_bad2 = "schlafen, schlafen, schlafen, schlafen, schlafen, schlafen, schlafen"
description_warning = "München und Berlin und Paris"

#result = evaluate_description(description_warning)
#print(result)

result = evaluate_description_http(description_bad1, 'de')