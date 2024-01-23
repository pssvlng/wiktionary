from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from ContextWord import ContextWord
from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam

from shared import *

def add_wordnet_annotations(g, subject, text, lang='de'):            
    exclusions = ['--',"'", "...", "…", "`", '"', '|', '-', '.', ':', '!', '?', ',', '%', '^', '(', ')', '$', '#', '@', '&', '*']
    context_uri = URIRef(f'{subject}_nif=context_char=0,{len(text)}')

    tag_results = tag_text(text, lang)
    wordTags = tag_results[0]
    named_entities = tag_results[1]                
    wordTags = merge_lists(named_entities, wordTags)        

    dict = Dictionary()
    merge_results = []
    for t in wordTags:            
        word = ContextWord()            
        word.name = t[0]
        word.whitespace = t[3]            
        word.isPropNoun = t[4]      
        word.linked_data = t[5]      
        word.lang = lang
        if len([x for x in ["'", "...", "…", "`", '"', '|'] if x in t[0]]) <= 0 and t[1] in ['VERB', 'NOUN', 'ADV', 'ADJ']:                
            word.pos = getSpacyToOliaPosMapping(t[1])                     
            word.lemma = t[2]

        merge_results.append(word)                  

    for index, value in enumerate(merge_results):         
        if value.lemma and value.pos and len(value.lemma) > 1 and value.lemma not in exclusions:               
            param = SearchParam()    
            param.lang = lang
            param.woi = value.lemma
            param.lemma = value.lemma
            param.pos = value.pos
            param.filterLang = lang    
            
            start_index = len(''.join([obj.name + obj.whitespace for obj in merge_results[:index]]))
            end_index = start_index + len(value.name)
            annotation_uri = URIRef(f'{subject}_a=spacy_char={start_index},{end_index}')            
            for item in value.linked_data:
                tup = spacy_to_olia[item]
                if tup:
                    add_unique_triple(g, annotation_uri, URIRef(tup[0]), URIRef(tup[1]))                    
            if value.isPropNoun:
                add_unique_triple(g, annotation_uri, RDF.type, URIRef(f'{lexinfo_uri}ProperNoun'))                                                                            
                dbnary_uri = get_dbnary_uri_prop_noun(value.lemma)                
            else:
                dbnary_uri = get_dbnary_uri(value.lemma, value.pos)                

            if dbnary_uri:
                    add_unique_triple(g, annotation_uri, itsrdf.taIdentRef, URIRef(dbnary_uri))    

            if len(dict.findWords(param)) == 0:                
                start_index = len(''.join([obj.name + obj.whitespace for obj in merge_results[:index]]))
                end_index = start_index + len(value.name)
                annotation_uri = URIRef(f'{subject}_a=spacy_char={start_index},{end_index}')                
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

def get_nif_literals_curriculum():        
    #nlp.max_length = 3000000
                         
    sparql = SPARQLWrapper("https://edu.yovisto.com/sparql")
    sparql_queries = [
    """
    select distinct * where {
                 ?s a <https://w3id.org/curriculum/CompetenceItem>  .
                 ?s <http://www.w3.org/2004/02/skos/core#prefLabel>  ?l .             
             }                                                            
    """,
    """
    select distinct * where {
                 ?s a <https://w3id.org/curriculum/FederalState>  .
                 ?s <http://www.w3.org/2004/02/skos/core#prefLabel>  ?l .                  
             }       
                                                     
    """,
    """
    select distinct * where {                                  
                ?s a <https://w3id.org/dini/dini-ns/Curriculum>  .
                ?s <http://www.w3.org/2004/02/skos/core#prefLabel>  ?l .           
             }       
                                                     
    """
    ]

    graph = Graph()
    for query in sparql_queries:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()    
        
        cntr = 0
        for result in results["results"]["bindings"]:
            subject = result["s"]["value"]                
            obj_prefLabel = result["l"]["value"]                            
            text = remove_html_tags_and_whitespace(obj_prefLabel)
            if text:                
                add_wordnet_annotations(graph, subject, text)
            cntr +=1
            if (cntr % 100 == 0):                                                
                print(f'{cntr} results of {len(results["results"]["bindings"])} processed')

    return graph    

#Main Program
graph = get_nif_literals_curriculum()            
output_file = "curricula_nif_dbnary.ttl"
graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')            

