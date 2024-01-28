from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD, SDO
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from ContextWord import ContextWord
from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam
from langdetect import detect
from datetime import datetime as dt
from shared import *
import sys
from collections import defaultdict

def add_wordnet_annotations_wlo(g, subject, name, description, keyword, keyword_key, lang):            
    context_uri_list = [
        {'p': 'name', 'text_to_annotate': name},
        {'p': 'description', 'text_to_annotate': description},
        {'p': f'{keyword_key}', 'text_to_annotate': keyword}                
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
            
            for index, value in enumerate(merge_results):         
                if value.lemma and value.pos and len(value.lemma) > 1 and value.lemma not in exclusions:   
                    dict = Dictionary()
                    param = SearchParam()    
                    param.lang = lang
                    param.woi = value.lemma
                    param.lemma = value.lemma
                    param.pos = value.pos
                    param.filterLang = lang    

                    start_index = len(''.join([obj.name + obj.whitespace for obj in merge_results[:index]]))
                    end_index = start_index + len(value.name)
                    annotation_uri = URIRef(f'{subject}_a=spacy_p={item["p"]}_char={start_index},{end_index}')            
                    lexinfo_pos = f'{lexinfo_uri}{value.pos}'
                    lexinfo_pos_prop = f'{lexinfo_uri}partOfSpeech'
                    add_unique_triple(g,annotation_uri, RDF.type, URIRef(lexinfo_pos))        
                    add_unique_triple(g,annotation_uri, URIRef(lexinfo_pos_prop), URIRef(lexinfo_pos))        
                    for grammar_item in value.linked_data:
                        tup = spacy_to_olia[grammar_item]
                        if tup:
                            add_unique_triple(g, annotation_uri, URIRef(tup[0]), URIRef(tup[1]))                    
                    if value.isPropNoun:
                        add_unique_triple(g, annotation_uri, RDF.type, URIRef(f'{lexinfo_uri}ProperNoun'))                                                                            
                        dbnary_uri = get_dbnary_uri_prop_noun(value.lemma)                
                    else:
                        dbnary_uri = get_dbnary_uri(value.lemma, value.pos)                
                    if dbnary_uri:
                        add_unique_triple(g, annotation_uri, itsrdf.termInfoRef, URIRef(dbnary_uri))        

                    if len(dict.findWords(param)) == 0:                                                                                    
                        olia_pos = f'{olia_uri}{value.pos.title()}'
                        
                        add_unique_triple(g,annotation_uri, RDF.type, nif.Phrase)                        
                        add_unique_triple(g,annotation_uri, RDF.type, URIRef(olia_pos))                                
                        add_unique_triple(g,annotation_uri, nif.beginIndex, Literal(start_index, datatype=XSD.nonNegativeInteger))
                        add_unique_triple(g,annotation_uri, nif.endIndex, Literal(end_index, datatype=XSD.nonNegativeInteger))
                        add_unique_triple(g,annotation_uri, nif.anchorOf, Literal(value.name))
                        add_unique_triple(g,annotation_uri, nif.predLang, URIRef(lexvo[lang]))
                        add_unique_triple(g,annotation_uri, nif.referenceContext, context_uri)                                       
                        add_unique_triple(g,annotation_uri, itsrdf.taAnnotatorsRef, URIRef('https://spacy.io'))                        

    return g        


def wlo_part_async(graph, results, thread_nr, lang=None):
    start_time = dt.now()
    cntr = 0        
    for result in results:
        subject = result["s"]["value"]                 
        name = remove_html_tags_and_whitespace(result["name"]["value"]) if 'name' in result else None               
        description = remove_html_tags_and_whitespace(result["description"]["value"]) if 'description' in result else None                                                
                        
        try:
            if description:
                lang = detect(description)                
            elif name:    
                lang = detect(name)                
        except:
            lang = 'en'
                            
        if (name or description) and lang == 'de':                            
            add_wordnet_annotations_wlo(graph, subject, name, description, None, '_', lang)
        cntr +=1
        if (cntr % 100 == 0):                                                
            print(f'{cntr} results of {len(results)} in thread {thread_nr} processed')
            end_time = dt.now()
            elapsed = end_time - start_time
            print(f'Running time for thread {thread_nr} (wlo): {elapsed.seconds // 3600}:{elapsed.seconds // 60 % 60}')
    
    return graph        

def get_keyword_key(subject):
    keyword_key_cntr[subject] += 1
    return f'keyword{keyword_key_cntr[subject]}'

def wlo_part_keywords_async(graph, results, thread_nr, lang=None):
    start_time = dt.now()
    cntr = 0        
    for result in results:
        subject = result["s"]["value"]                         
        keyword = remove_html_tags_and_whitespace(result["keywords"]["value"]) if 'keywords' in result else None                                        
                        
        # try:
        #     if keyword:
        #         lang = detect(keyword)                
        # except:
        #     lang = 'en'
        lang = 'de'
                            
        if (keyword) and lang == 'de':                
            key = get_keyword_key(subject)            
            add_wordnet_annotations_wlo(graph, subject, None, None, keyword, key, lang)
        cntr +=1
        if (cntr % 100 == 0):                                                
            print(f'{cntr} results of {len(results)} in thread {thread_nr} processed')
            end_time = dt.now()
            elapsed = end_time - start_time
            print(f'Running time for thread {thread_nr} (kewords): {elapsed.seconds // 3600}:{elapsed.seconds // 60 % 60}')
    
    return graph            

def get_nif_literals_wlo_keywords_async(thread_cnt, thread_nr):
    sparql = SPARQLWrapper("https://edu.yovisto.com/sparql")
    list_length = 1140255
    part_length = list_length // thread_cnt    
    query = """
    select distinct * where {                                                                   
                OPTIONAL { 
                    ?s <https://schema.org/keywords> ?keywords . 
                }                 
             }                            
    """ 
    query += f'LIMIT {part_length} OFFSET {part_length * thread_nr}'

    graph = Graph()            
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]    
    graph = wlo_part_keywords_async(graph, results, thread_nr)                

    return graph

def get_nif_literals_wlo_async(thread_cnt, thread_nr):
    nlp['de'].max_length = 3000000
                         
    sparql = SPARQLWrapper("https://edu.yovisto.com/sparql")
    list_length = 164843
    part_length = list_length // thread_cnt    
    query = """
    select distinct * where {                                  
                ?s a <https://edu.yovisto.com/ontology/wlo/Resource>  .
                OPTIONAL { 
                    ?s <https://schema.org/name>  ?name . 
                }         
                OPTIONAL { 
                    ?s <https://schema.org/description> ?description . 
                }                                                  
             }                            
    """ 
    query += f'LIMIT {part_length} OFFSET {part_length * thread_nr}'

    graph = Graph()            
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]        
    graph = wlo_part_async(graph, results, thread_nr)                

    return graph

def get_nif_literals_wlo():
    #nlp.max_length = 3000000
                         
    sparql = SPARQLWrapper("https://edu.yovisto.com/sparql")
    sparql_queries = [    
    """
    select distinct * where {                                  
                ?s a <https://edu.yovisto.com/ontology/wlo/Resource>  .
                OPTIONAL { 
                    ?s <https://schema.org/name>  ?name . 
                }         
                OPTIONAL { 
                    ?s <https://schema.org/description> ?description . 
                }                 
                OPTIONAL { 
                    ?s <https://schema.org/keywords> ?keywords . 
                }                 
             }                           
     
    """
    ]
    
    start_time = dt.now()

    graph = Graph()
    for query in sparql_queries:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()    
        
        cntr = 0
        for result in results["results"]["bindings"]:
            subject = result["s"]["value"]                
            name = result["name"]["value"]                
            description = result["description"]["value"]                                        
            keywords = result["keywords"]["value"]                                        
            name = remove_html_tags_and_whitespace(name)
            description = remove_html_tags_and_whitespace(description)            
            keywords = remove_html_tags_and_whitespace(keywords)            
            lang = 'en'
            if description:
                lang = detect(description)                
            elif name:    
                lang = detect(name)
            elif keywords:
                lang = detect(keywords)
                    
            if lang not in ['en', 'de']:
                    lang = 'en'        
            if (name or description or keywords) and lang == 'de':                                
                add_wordnet_annotations_wlo(graph, subject, name, description, keywords, lang)
            cntr +=1
            if (cntr % 100 == 0):                                                
                print(f'{cntr} results of {len(results["results"]["bindings"])} processed')
                end_time = dt.now()
                elapsed = end_time - start_time
                print(f'Running time: {elapsed.seconds // 3600}:{elapsed.seconds // 60 % 60}')

    return graph       
                               

#Main Program
CONTEXT_MARGIN = 15

if len(sys.argv) == 4:
    thread_cnt = int(sys.argv[1])
    thread_nr = int(sys.argv[2])
    category = sys.argv[3]

    if category == 'wlo':
        graph = get_nif_literals_wlo_async(thread_cnt, thread_nr)            
        output_file = f"wlo_nif_{thread_nr}.ttl"    
        graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')            
    
    if category == 'keywords':
        keyword_key_cntr = defaultdict(int)
        graph = get_nif_literals_wlo_keywords_async(thread_cnt, thread_nr)            
        output_file = f"wlo_nif_keywords_{thread_nr}.ttl"    
        graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')            
        
else:
    graph = get_nif_literals_wlo()            
    output_file = "wlo_nif.ttl"    
    graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')          



