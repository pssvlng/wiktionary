from collections import defaultdict
import json
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, SKOS 

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def build_tree(graph: Graph):    
    tree = {}
    for subj, pred, obj in graph.triples((None, None, None)):
        item_id = str(subj)        
        
        if item_id not in tree:
            tree[item_id] = []            
        else:
            tree[item_id].append((str(pred), str(obj)))            

    return tree

def print_tree_to_file(dict, output_file):
    def get_short_str(string):    
        last_backslash_index = string.rfind('/')            
        if last_backslash_index != -1:            
            return string[last_backslash_index + 1:]
        else:            
            return string 
        
    with open(output_file, "w") as f:
        for key, value in dict.items():            
            new_key = get_short_str(key) 
            f.write(new_key + ';"";""\n')
            for item in value:
                f.write(f'"";{get_short_str(item[0])};{get_short_str(item[1])}\n')
    
if __name__ == "__main__":
    # Example usage
    input_ttl_file = 'input.ttl'
    output_csv_file = 'output.csv'
    output_txt_file = 'output.txt'
    output_xlsx_file = 'output.xlsx'
    #ttl_to_csv(input_ttl_file, output_csv_file)
    g = Graph()
    g.parse(input_ttl_file, format='turtle')
    
    tree = build_tree(g)
    print_tree_to_file(tree, output_csv_file)