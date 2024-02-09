from collections import defaultdict
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD, SDO
from queries_en import WORDNET_RDF_2, WORDNET_RDF, WORDNET_RDF_3, WORDNET_RDF_CNT
from shared import *

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

def get_annotation_text_example(graph, limit: int, offset: int, db_name:str):    
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    query = WORDNET_RDF_2
    query = query.replace('{LIMIT_VAR}', str(limit))
    query = query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    
    cntr = 0    
    for result in results["results"]["bindings"]:
        example_key = get_example_key(result["synset"]["value"])
        add_nif_context(graph, result["synset"]["value"], None, None, result["example"]["value"], example_key, 'en')
        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    

def get_annotation_text_def(graph, limit: int, offset: int, db_name:str):    
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    query = WORDNET_RDF_3
    query = query.replace('{LIMIT_VAR}', str(limit))
    query = query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    
    cntr = 0        
    for result in results["results"]["bindings"]:
        definition_key = get_definition_key(result["synset"]["value"])
        add_nif_context(graph, result["synset"]["value"], result["def"]["value"], definition_key, None, None, 'en')
        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    
   
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
        get_annotation_text_def(graph, limit, offset, db_name)    
        output_file = f"wordnet_en_definitions_{thread_nr}.ttl"    
        graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')          
    
    if category == "example":
        #range: 0-6        
        offset = limit * thread_nr  
        graph = Graph()
        get_annotation_text_example(graph, limit, offset, db_name)
        output_file = f"wordnet_en_examples_{thread_nr}.ttl"    
        graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')          

