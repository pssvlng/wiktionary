from collections import defaultdict
import csv
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import OWL, SKOS, Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD, SDO
import requests
from ContextWord import ContextWord
from WeightedWord import WeightedWord
from queries_en import GET_WIKIDATA_ALL_MISMATCH_ID, GET_WIKIDATA_CLASSES, GET_WIKIDATA_MISMATCH, GET_WIKIDATA_URI, LOD_CLOSE_MATCHES, SYNSET_NOUNS_STAGING_CREATE, SYNSET_NOUNS_STAGING_INSERT, SYNSET_NOUNS_STAGING_SELECT, SYNSET_NOUNS_STAGING_UPDATE, WIKIDATA_CLASSES_INSERT, WORDNET_RDF_2, WORDNET_RDF, WORDNET_RDF_3, WORDNET_RDF_4, WORDNET_RDF_CNT
from shared import *
from SimilarityClassifier import SimilarityClassifier
from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam
import wn

def get_wordnet_annotation_text_cnt():
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    query = WORDNET_RDF_CNT        
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    print(results)

def get_definition_key(subject):
    definition_key_cntr[subject] += 1
    return f'definition{definition_key_cntr[subject]}'

def get_example_key(subject):
    example_key_cntr[subject] += 1
    return f'example{example_key_cntr[subject]}'

def add_nif_context(g, subject, definition, definition_key, example, example_key, lang):
    sub = URIRef(subject)                       
        
    if definition:
        context_uri = URIRef(f'{subject}_nif=context_p={definition_key}_char=0,{len(definition)}')
        add_unique_triple(g,context_uri, RDF.type, nif.Context)        
        add_unique_triple(g,context_uri, nif.beginIndex, Literal(0, datatype=XSD.nonNegativeInteger))
        add_unique_triple(g,context_uri, nif.endIndex, Literal(len(definition), datatype=XSD.nonNegativeInteger))
        add_unique_triple(g,context_uri, nif.isString, Literal(definition, lang=lang))
        add_unique_triple(g,context_uri, nif.predLang, URIRef(lexvo[lang]))        
        add_unique_triple(g,context_uri, nif.wasConvertedFrom, wn_ns.definition)    
        add_unique_triple(g,sub, curriculum_ns.hasAnnotationTarget, context_uri)
        add_unique_triple(g,context_uri, curriculum_ns.isAnnotationTargetOf, sub)

    if example:
        context_uri = URIRef(f'{subject}_nif=context_p={example_key}_char=0,{len(example)}')
        add_unique_triple(g,context_uri, RDF.type, nif.Context)        
        add_unique_triple(g,context_uri, nif.beginIndex, Literal(0, datatype=XSD.nonNegativeInteger))
        add_unique_triple(g,context_uri, nif.endIndex, Literal(len(example), datatype=XSD.nonNegativeInteger))
        add_unique_triple(g,context_uri, nif.isString, Literal(example, lang=lang))
        add_unique_triple(g,context_uri, nif.predLang, URIRef(lexvo[lang]))        
        add_unique_triple(g,context_uri, nif.wasConvertedFrom, wn_ns.example)    
        add_unique_triple(g,sub, curriculum_ns.hasAnnotationTarget, context_uri)
        add_unique_triple(g,context_uri, curriculum_ns.isAnnotationTargetOf, sub)    

    return g

def add_dbpedia_annotations(g, subject, definition, definition_key, example, example_key, lang):                                                    
    context_uri_list = [        
        {'p': f'{definition_key}', 'text_to_annotate': definition},   
        {'p': f'{example_key}', 'text_to_annotate': example}                     
    ]

    for item in context_uri_list:

        text_to_annotate = item['text_to_annotate']
        if text_to_annotate:
            context_uri = URIRef(f'{subject}_nif=context_p={item["p"]}_char=0,{len(text_to_annotate)}')

            headers = {
                "Accept": "application/json",
            }
            
            params = {
                "text": text_to_annotate,
            }
            try:
                response = requests.get(spotlight_url[lang], params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()        
                    annotations = data.get("Resources", [])

                    for _, annotation in enumerate(annotations, start=1):            
                        surface_form = annotation.get("@surfaceForm", "")
                        start_index = int(annotation.get("@offset", 0))
                        end_index = start_index + len(surface_form)
                        annotation_uri = URIRef(f'{subject}_a=dbpedia-spotlight_p={item["p"]}_char={start_index},{end_index}')
                        dbpedia_resource = URIRef(annotation.get("@URI", ""))
                        
                        add_unique_triple(g,annotation_uri, RDF.type, nif.Phrase)                        
                        add_unique_triple(g,annotation_uri, nif.beginIndex, Literal(start_index, datatype=XSD.nonNegativeInteger))
                        add_unique_triple(g,annotation_uri, nif.endIndex, Literal(end_index, datatype=XSD.nonNegativeInteger))
                        add_unique_triple(g,annotation_uri, nif.anchorOf, Literal(surface_form))
                        add_unique_triple(g,annotation_uri, nif.predLang, URIRef(lexvo[lang]))
                        add_unique_triple(g,annotation_uri, nif.referenceContext, context_uri)
                        add_unique_triple(g,annotation_uri, itsrdf.taAnnotatorsRef, URIRef('http://www.dbpedia-spotlight.org'))
                        add_unique_triple(g,annotation_uri, itsrdf.taConfidence, Literal(annotation.get("@similarityScore", "0")))
                        add_unique_triple(g,annotation_uri, itsrdf.taIdentRef, dbpedia_resource)                                
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            except:
                pass
    return g    

def add_wordnet_annotations(g, subject, definition, definition_key, example, example_key, lang):              
    context_uri_list = [        
        {'p': f'{definition_key}', 'text_to_annotate': definition},        
        {'p': f'{example_key}', 'text_to_annotate': example}                
    ]
    exclusions = ['--',"'", "...", "…", "`", '"', '|', '-', '.', ':', '!', '?', ',', '%', '^', '(', ')', '$', '#', '@', '&', '*']
    
    for item in context_uri_list:
        if item["text_to_annotate"]:
            context_uri = URIRef(f'{subject}_nif=context_p={item["p"]}_char=0,{len(item["text_to_annotate"])}')

            tag_results = tag_text(item["text_to_annotate"], lang)
            wordTags = tag_results[0]
            dbpedia_entities = tag_results[1]                
            wordTags = merge_lists(dbpedia_entities, wordTags)        

            merge_results = []
            for t in wordTags:            
                word = ContextWord()            
                word.name = t[0]
                word.whitespace = t[3]            
                word.isPropNoun = t[4]      
                word.linked_data = t[5]      
                word.lang = lang
                                
                if len([x for x in exclusions if x in t[0]]) <= 0 and t[1] in ['VERB', 'NOUN', 'ADV', 'ADJ']:                
                    word.pos = getSpacyToOliaPosMapping(t[1])                     
                    word.lemma = t[2]

                merge_results.append(word)                                

            classifier = SimilarityClassifier(nlp[lang])              
            for index, value in enumerate(merge_results):         
                if value.lemma and value.pos and len(value.lemma) > 1 and value.lemma not in exclusions:   
                    dict = Dictionary()
                    param = SearchParam()    
                    param.lang = lang
                    param.woi = value.lemma
                    param.lemma = value.lemma
                    param.pos = value.pos
                    param.filterLang = lang    
                    words = dict.findWords(param);

                    weighted_words = []
                    
                    if len(words) > 100:
                        print(f"{value.lemma} - {value.pos} > 100 results")

                    for word in words[:30]:
                        weighted_word = WeightedWord(word)                          
                        start_idx = 0 if index - CONTEXT_MARGIN < 0 else index - CONTEXT_MARGIN
                        end_idx = len(merge_results) if index + CONTEXT_MARGIN >= len(merge_results) else index + CONTEXT_MARGIN
                        sub_text = ' '.join([x.name for x in merge_results[start_idx:end_idx]])                  
                        words_to_compare = word_compare_lookup[f'{lang}_0'][f'{lang}-0-{word.ili}']                                         
                        weighted_word.weight = classifier.classify(sub_text, words_to_compare)                    
                        weighted_words.append(weighted_word)

                    start_index = len(''.join([obj.name + obj.whitespace for obj in merge_results[:index]]))
                    end_index = start_index + len(value.name)                        
                    annotation_uri = URIRef(f'{subject}_a=spacy_p={item["p"]}_char={start_index},{end_index}')
                    lexinfo_pos = f'{lexinfo_uri}{value.pos}'
                    lexinfo_pos_prop = f'{lexinfo_uri}partOfSpeech'
                    add_unique_triple(g,annotation_uri, RDF.type, URIRef(lexinfo_pos))        
                    add_unique_triple(g,annotation_uri, URIRef(lexinfo_pos_prop), URIRef(lexinfo_pos))        
                    # for grammar_item in value.linked_data:
                    #     tup = spacy_to_olia[grammar_item]
                    #     if tup:
                    #         add_unique_triple(g, annotation_uri, URIRef(tup[0]), URIRef(tup[1]))                    
                    # if value.isPropNoun:
                    #     add_unique_triple(g, annotation_uri, RDF.type, URIRef(f'{lexinfo_uri}ProperNoun'))                                                                            
                    #     dbnary_uri = get_dbnary_uri_prop_noun(value.lemma, 'en')                
                    # else:
                    dbnary_uri = get_dbnary_uri(value.lemma, value.pos, 'en')                
                    if dbnary_uri:
                        add_unique_triple(g, annotation_uri, itsrdf.termInfoRef, URIRef(dbnary_uri))        

                    if len(weighted_words) > 0:                        
                        selected_word = max(weighted_words, key=lambda obj: obj.weight).word                            
                        ili = f'{ili_uri}{selected_word.ili}'
                        ili_en = f'{ili_en_uri}{selected_word.ili}'
                        olia_pos = f'{olia_uri}{selected_word.pos}'

                        add_unique_triple(g,annotation_uri, RDF.type, nif.Phrase)                        
                        add_unique_triple(g,annotation_uri, RDF.type, URIRef(olia_pos))        
                        add_unique_triple(g,annotation_uri, nif.beginIndex, Literal(start_index, datatype=XSD.nonNegativeInteger))
                        add_unique_triple(g,annotation_uri, nif.endIndex, Literal(end_index, datatype=XSD.nonNegativeInteger))
                        add_unique_triple(g,annotation_uri, nif.anchorOf, Literal(value.name))
                        add_unique_triple(g,annotation_uri, nif.predLang, URIRef(lexvo[lang]))
                        add_unique_triple(g,annotation_uri, nif.referenceContext, context_uri)                                       
                        add_unique_triple(g,annotation_uri, itsrdf.taAnnotatorsRef, URIRef('https://spacy.io'))
                        add_unique_triple(g,annotation_uri, itsrdf.taIdentRef, URIRef(ili))
                        add_unique_triple(g,annotation_uri, itsrdf.taIdentRef, URIRef(ili_en))                        

    return g   

def get_annotation_text_example(graph, limit: int, offset: int):    
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    query = WORDNET_RDF_2
    query = query.replace('{LIMIT_VAR}', str(limit))
    query = query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    
    cntr = 0    
    for result in results["results"]["bindings"]:
        subject = result["synset"]["value"]
        example = result["example"]["value"]        
        example_key = get_example_key(result["synset"]["value"])
        add_nif_context(graph, subject, None, None, example, example_key, 'en')
        add_dbpedia_annotations(graph, subject, None, None, example, example_key, 'en')
        add_wordnet_annotations(graph, subject, None, None, example, example_key, 'en')
        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    

def get_annotation_text_def(graph, limit: int, offset: int):    
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    query = WORDNET_RDF_3
    query = query.replace('{LIMIT_VAR}', str(limit))
    query = query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    
    cntr = 0        
    for result in results["results"]["bindings"]:
        subject = result["synset"]["value"]
        definition = result["def"]["value"]
        definition_key = get_definition_key(subject)
        add_nif_context(graph, subject, definition, definition_key, None, None, 'en')
        add_dbpedia_annotations(graph, subject, definition, definition_key, None, None, 'en')
        add_wordnet_annotations(graph, subject, definition, definition_key, None, None, 'en')
        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    

def get_loduri_for_lemmas(graph, limit: int, offset: int):    
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    query = WORDNET_RDF_4
    query = query.replace('{LIMIT_VAR}', str(limit))
    query = query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    
    cntr = 0        
    for result in results["results"]["bindings"]:
        lex_entry = result["lexEntry"]["value"]
        written_rep = result["writtenRep"]["value"].upper()
        pos = result["pos"]["value"]
        if pos in ["https://globalwordnet.github.io/schemas/wn#adjective", "https://globalwordnet.github.io/schemas/wn#adjective_satellite"]:
            dbnary_lex_entry = adjective_lookup['en'][written_rep]            
            if dbnary_lex_entry:
                lex_entry = lex_entry.replace('#', '_')                
                lex_entry = lex_entry.replace('https://en-word.net/', 'https://edu.yovisto.com/resource/wordnet/en/')
                add_unique_triple(graph, URIRef(lex_entry), OWL.sameAs, URIRef(dbnary_lex_entry))                        
        if pos == "https://globalwordnet.github.io/schemas/wn#noun":
            dbnary_lex_entry = noun_lookup['en'][written_rep]
            if not dbnary_lex_entry:
                dbnary_lex_entry = proper_noun_lookup['en'][written_rep]
            if dbnary_lex_entry:
                lex_entry = lex_entry.replace('#', '_')
                lex_entry = lex_entry.replace('https://en-word.net/', 'https://edu.yovisto.com/resource/wordnet/en/')
                add_unique_triple(graph, URIRef(lex_entry), OWL.sameAs, URIRef(dbnary_lex_entry))                        
        if pos == "https://globalwordnet.github.io/schemas/wn#verb":
            dbnary_lex_entry = verb_lookup['en'][written_rep]            
            if dbnary_lex_entry:
                lex_entry = lex_entry.replace('#', '_')
                lex_entry = lex_entry.replace('https://en-word.net/', 'https://edu.yovisto.com/resource/wordnet/en/')
                add_unique_triple(graph, URIRef(lex_entry), OWL.sameAs, URIRef(dbnary_lex_entry))                        
        if pos == "https://globalwordnet.github.io/schemas/wn#adverb":
            dbnary_lex_entry = adverb_lookup['en'][written_rep]            
            if dbnary_lex_entry:
                lex_entry = lex_entry.replace('#', '_')
                lex_entry = lex_entry.replace('https://en-word.net/', 'https://edu.yovisto.com/resource/wordnet/en/')
                add_unique_triple(graph, URIRef(lex_entry), OWL.sameAs, URIRef(dbnary_lex_entry))                        

        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    


def get_lemma_same_as(graph, limit: int, offset: int, source_prefix:str, target_prefix:str, query:str):
    results = get_same_as(limit, offset, query)
    cntr = 0        
    for result in results["results"]["bindings"]:
        lemma = result["lexEntry"]["value"]
        subject = lemma.replace(source_prefix, target_prefix)        
        add_unique_triple(graph, URIRef(subject), OWL.sameAs, URIRef(lemma))                        

        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    

def get_synset_same_as(graph, limit: int, offset: int, source_prefix:str, target_prefix:str, query:str):
    results = get_same_as(limit, offset, query)
    cntr = 0        
    for result in results["results"]["bindings"]:
        synset = result["synset"]["value"]
        subject = synset.replace(source_prefix, target_prefix)
        add_unique_triple(graph, URIRef(subject), OWL.sameAs, URIRef(synset))                        

        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    

def get_same_as(limit: int, offset: int, query:str):    
    sparql = SPARQLWrapper("http://localhost:8890/sparql")    
    query = query.replace('{LIMIT_VAR}', str(limit))
    query = query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()    
    
def add_dbpedia_annotations_synsets(lang):                                                        
    db_name = f"synset_noun_{lang}.db"
    conn = sqlite3.connect(db_name)    
    conn.execute(SYNSET_NOUNS_STAGING_CREATE)    
    conn.close()

    cntr = 0    
    synsets = wn.synsets(pos='n', lang='en')
    data_to_insert = []
    for synset in synsets:
        definition = synset.definition()
        examples = [definition]
        for example in synset.examples():
            if example:
                examples.append(example)

        for lemma in synset.lemmas():
            spotlight_str = f'{lemma}: {". ".join(examples)}'
            headers = {
                "Accept": "application/json",
            }
            
            params = {
                "text": spotlight_str
            }
            try:
                response = requests.get(spotlight_url[lang], params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()        
                    annotations = data.get("Resources", [])

                    for _, annotation in enumerate(annotations, start=1):            
                        surface_form = annotation.get("@surfaceForm", "")
                        start_index = int(annotation.get("@offset", 0))
                        if start_index == 0 and surface_form == lemma:
                            dbpedia_resource = annotation.get("@URI", "")
                            confidence = annotation.get("@similarityScore", "0")
                            data_to_insert.append((synset.id, synset.ili.id, lemma, spotlight_str, dbpedia_resource, confidence, "0"))                            
                                                
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            except:
                pass
        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(synsets)}')
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.executemany(SYNSET_NOUNS_STAGING_INSERT, data_to_insert)
            conn.commit()
            conn.close()
            data_to_insert = []

def add_dbpedia_annotations_synsets(g, source_prefix, lang):
    db_name = f"synset_noun_{lang}.db"
    conn = sqlite3.connect(db_name)    
    cursor = conn.cursor()
    cursor.execute(LOD_CLOSE_MATCHES)
    rows = cursor.fetchall()
    cntr = 0
    for row in rows:        
        wiki_data_verified = row[4]
        if wiki_data_verified:
            add_unique_triple(g, URIRef(f'{source_prefix}{row[0]}'), SKOS.closeMatch, URIRef(f'{wiki_data_verified}'))     
        else:
            add_unique_triple(g, URIRef(f'{source_prefix}{row[0]}'), SKOS.closeMatch, URIRef(f'{row[3]}'))         
        add_unique_triple(g, URIRef(f'{source_prefix}{row[0]}'), SKOS.closeMatch, URIRef(f'{row[2]}')) 
        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(rows)}')
    conn.close()
    return g

def add_wikidata_links_synsets(lang):
    db_name = f"synset_noun_{lang}.db"
    conn = sqlite3.connect(db_name)    
    cursor = conn.cursor()
    cursor.execute("select * from SYNSET_NOUNS_STAGING where wikidata IS NULL")
    rows = cursor.fetchall()    
    cntr = 0
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    result_list = []
    for row in rows:                
        query = GET_WIKIDATA_URI
        query = query.replace('{DB_PEDIA_URI}', row[4])        
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()            
        try:
            wikidata_uri = results["results"]["bindings"][0]["wikidataUri"]["value"]                        
            result_list.append((wikidata_uri, row[4]))            
        except Exception as e:
            print(f"WikiData Uri not found for: {row[4]}")    
            print(e)                
        cntr += 1

        if (cntr % 1000 == 0):          
            cursor.executemany(SYNSET_NOUNS_STAGING_UPDATE, result_list)
            conn.commit()                          
            print(f'Records processed: {cntr} of {len(rows)}')
            result_list.clear()

    cursor.executemany(SYNSET_NOUNS_STAGING_UPDATE, result_list)
    conn.commit()                          
    print(f'Records processed: {cntr} of {len(rows)}')    
    conn.close()
    
def compare_wikidata_classes(lang):
    db_name = f"synset_noun_{lang}.db"
    conn = sqlite3.connect(db_name)    
    cursor = conn.cursor()
    cursor.execute(GET_WIKIDATA_ALL_MISMATCH_ID)
    rows = cursor.fetchall()    
    cntr = 2000
    data_to_insert = []
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")                    
    for row in rows[2000:]:           
        query = GET_WIKIDATA_CLASSES
        query = query.replace('{WIKIDATA_URI}', row[0])        
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()   
        
        for result in results["results"]["bindings"]:
            data_to_insert.append((row[0], result["o"]["value"]))        

        cntr += 1    
        if (cntr % 100 == 0):                          
            cursor.executemany(WIKIDATA_CLASSES_INSERT, data_to_insert)
            conn.commit()                          
            print(f'Records processed: {cntr} of {len(rows)}')
            data_to_insert.clear()

    cursor.executemany(WIKIDATA_CLASSES_INSERT, data_to_insert)
    conn.commit()                          
    print(f'Records processed: {cntr} of {len(rows)}')            
    conn.close()

def analyse_wikidata_classes(lang, file_path):
    result_dict = {}
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = row[0], row[1]            
            if key in result_dict:                
                result_dict[key.strip()].add(value.strip())
            else:                
                result_dict[key.strip()] = {key.strip(), value.strip()}
    match_cntr = 0
    errs = 0
    db_name = f"synset_noun_{lang}.db"
    conn = sqlite3.connect(db_name)    
    cursor = conn.cursor()
    cursor.execute(GET_WIKIDATA_MISMATCH)
    rows = cursor.fetchall()            
    for row in rows:       
        try:                  
            set1 = result_dict[row[5]]
            set2 = result_dict[row[6]]
            if len(set1.intersection(set2)) > 0:
                match_cntr += 1
            else:
                print(set1)
                print(set2)
                print()    
        except Exception as e:    
            errs += 1

    print(f"matches: {match_cntr}")
    print(f"errors: {errs}")

CONTEXT_MARGIN = 15   
db_name = "wiktionary_en.db"
limit = 10000
definition_key_cntr = defaultdict(int)
example_key_cntr = defaultdict(int)

if len(sys.argv) == 4:
    thread_cnt = int(sys.argv[1])
    thread_nr = int(sys.argv[2])
    category = sys.argv[3]

    if category == "definition":
        #range: 0-13        
        offset = limit * thread_nr
        graph = Graph()
        get_annotation_text_def(graph, limit, offset)    
        output_file = f"wordnet_en_definitions_{thread_nr}.ttl"    
        graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')          
    
    if category == "example":
        #range: 0-6        
        offset = limit * thread_nr  
        graph = Graph()
        get_annotation_text_example(graph, limit, offset)
        output_file = f"wordnet_en_examples_{thread_nr}.ttl"    
        graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')          

    if category == "lemma":
        print("Starting Canon Form Insert ...")
        for x in range(0,17):                
            offset = 10000 * x                
            graph = Graph()
            get_loduri_for_lemmas(graph, limit, offset)
            output_file = f"wordnet_en_lod_lemmas_{x}.ttl"    
            graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')    

    if category == "lemma_same_as":
        print("Starting lemmas_same_as triples ...")
        for x in range(0,17):                
            offset = 10000 * x                
            graph = Graph()
            target_prefix = 'https://edu.yovisto.com/resource/wordnet/en/'
            source_prefix = 'https://en-word.net/'            
            query = WORDNET_RDF_4
            get_lemma_same_as(graph, limit, offset, source_prefix, target_prefix, query)
            output_file = f"wordnet_en_lemmas_same_as{x}.ttl"    
            graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')    

    if category == "synset_same_as":
        print("Starting synset_same_as triples ...")
        for x in range(0,13):                
            offset = 10000 * x                
            graph = Graph()
            target_prefix = 'https://edu.yovisto.com/resource/wordnet/en/'
            source_prefix = 'https://en-word.net/'            
            query = WORDNET_RDF_3
            get_synset_same_as(graph, limit, offset, source_prefix, target_prefix, query)
            output_file = f"wordnet_en_synsets_same_as{x}.ttl"    
            graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')    

    if category == "dbpedia_synset":        
        lang = 'en'
        add_dbpedia_annotations_synsets(lang)

    if category == "dbpedia_synset_same_as":
        graph = Graph()
        lang = 'en'
        source_prefix = 'https://edu.yovisto.com/resource/wordnet/en/id/o'
        add_dbpedia_annotations_synsets(graph, source_prefix, lang)
        output_file = output_file = f"dbpedia_synset_same_as_{lang}.ttl"                    
        graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')    

    if category == "dbpedia_synset_wikidata":      
        lang = 'en'  
        analyse_wikidata_classes(lang, "wikidata_classes_distinct.csv")
        #compare_wikidata_classes(lang)
        #add_wikidata_links_synsets(lang)