import shutil
import os
from SPARQLWrapper import JSON, SPARQLWrapper
from rdflib import OWL, Graph, Literal, URIRef
from queries_en import WORDNET_RDF_OBJECT_HASHED, WORDNET_RDF_SUBJECT_HASHED
from shared import add_unique_triple

def replace_in_files(directory, search_string, replace_string):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
                        
            if file_path.endswith('.ttl'):            
                with open(file_path, 'r') as f:
                    content = f.read()
                                
                modified_content = content.replace(search_string, replace_string)
                                
                with open(file_path, 'w') as f:
                    f.write(modified_content)
                
                print(f"Modified: {file_path}")

def copy_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        source_file = os.path.join(input_folder, filename)
        dest_file = os.path.join(output_folder, filename)
                
        shutil.copy2(source_file, dest_file)
        print(f"Copied {source_file} to {dest_file}")

def get_query(query, limit, offset):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    query = query
    query = query.replace('{LIMIT_VAR}', str(limit))
    query = query.replace('{OFFSET_VAR}', str(offset))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()    

def get_unhashed_triples_subject(graph, limit, offset, source_prefix, target_prefix, query):
    results = get_query(query, limit, offset)    
    cntr = 0        
    for result in results["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        subject = result["subject"]["value"]
        subject = subject.replace(source_prefix, target_prefix)
        subject = subject.replace('#', '_')
        object = result["object"]["value"]
        if object.startswith(source_prefix):
            object = object.replace(source_prefix, target_prefix)
            object = object.replace('#', '_')

        if result["object"]["type"] == 'uri':        
            add_unique_triple(graph, URIRef(subject), URIRef(predicate), URIRef(object))                      
        else:    
            add_unique_triple(graph, URIRef(subject), URIRef(predicate), Literal(object, lang='en'))
        original_subject = result["subject"]["value"]

        new_subject = original_subject.replace(source_prefix, target_prefix)
        add_unique_triple(graph, URIRef(subject), OWL.sameAs, URIRef(new_subject))                        
        add_unique_triple(graph, URIRef(subject), OWL.sameAs, URIRef(original_subject))                        
        add_unique_triple(graph, URIRef(new_subject), OWL.sameAs, URIRef(subject))                        

        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    

def get_unhashed_triples_object(graph, limit, offset, source_prefix, target_prefix, query):
    results = get_query(query, limit, offset)    
    cntr = 0        
    for result in results["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        subject = result["subject"]["value"]
        if subject.startswith(source_prefix):
            subject = subject.replace(source_prefix, target_prefix)
            subject = subject.replace('#', '_')
        object = result["object"]["value"]        
        object = object.replace(source_prefix, target_prefix)
        object = object.replace('#', '_')
            
        add_unique_triple(graph, URIRef(subject), URIRef(predicate), URIRef(object))                        
        
        cntr += 1
        if (cntr % 1000 == 0):
            print(f'Records processed: {cntr} of {len(results["results"]["bindings"])}')

    return graph    

def get_wikidata_mappings(db_name):
    pass

# limit = 10000
# for x in range(119,150):                
#     graph = Graph()
#     offset = limit * x                    
#     target_prefix = 'https://edu.yovisto.com/resource/wordnet/en/'
#     source_prefix = 'https://en-word.net/'            
#     query = WORDNET_RDF_SUBJECT_HASHED
#     get_unhashed_triples_subject(graph, limit, offset, source_prefix, target_prefix, query)
#     output_file = f"wordnet_en_hashed_subject_{x}.ttl"    
#     graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')    

# for x in range(0,17):                
#     graph = Graph()
#     offset = limit * x                    
#     target_prefix = 'https://edu.yovisto.com/resource/wordnet/en/'
#     source_prefix = 'https://en-word.net/'            
#     query = WORDNET_RDF_OBJECT_HASHED
#     get_unhashed_triples_object(graph, limit, offset, source_prefix, target_prefix, query)
#     output_file = f"wordnet_en_hashed_object_{x}.ttl"    
#     graph.serialize(destination=output_file, format="turtle", encoding='UTF-8')    

#source_directory = 'prefix_en-wordnet_1'
#destination_directory = 'prefix_yovisto'
#copy_files(source_directory, destination_directory)
#search_string = 'https://edu.yovisto.com/resource/wordnet/en/ili/'
#replace_string = 'https://en-word.net/ili/'
#replace_in_files(destination_directory, search_string, replace_string)    