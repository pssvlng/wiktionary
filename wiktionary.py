from collections import defaultdict
import os
import mwxml
import mwparserfromhell
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD, RDFS
from SPARQLWrapper import SPARQLWrapper, JSON

from shared import add_unique_triple, olia_uri

allowed_pos = ['verb', 'adjektiv', 'adverb', 'substantiv']

def get_template(templates, value):
    return next((template for template in templates if template.name.lower() == value.lower()), None)    

def get_template_contains(templates, value):
    return next((template for template in templates if value.lower() in template.name.lower()), None)    

def clean_element(dirty_str):
    clean_str = dirty_str.replace('\n', '')
    return clean_str

def params_to_dict(params):
    result = {}
    for param in params:
        param = clean_element(param)
        key_value = param.split("=")
        if len(key_value) == 2:
            result[key_value[0]] = key_value[1]

    return result    

def get_resource_key(category) -> int:
    resource_cntr[category] += 1
    return resource_cntr[category]

def add_triples(graph, lemma, pos, form):
    if (pos.lower() == "verb"):
        sub = URIRef(f'http://container1:8080/wictionary/resource/Verb/{get_resource_key("Verb")}')                    
        obj = URIRef(f'{olia_uri}Verb')
        add_unique_triple(graph, sub, RDF.type, obj)
        add_unique_triple(graph, sub, RDFS.label, Literal(lemma, lang='de'))

        return
    if (pos.lower() == "adverb"):
        sub = URIRef(f'http://container1:8080/wictionary/resource/Adverb/{get_resource_key("Adverb")}')                    
        obj = URIRef(f'{olia_uri}Adverb')
        add_unique_triple(graph, sub, RDF.type, obj)        
        return
    if (pos.lower() == "adjectiv"):
        sub = URIRef(f'http://container1:8080/wictionary/resource/Adjective/{get_resource_key("Adjective")}')                    
        obj = URIRef(f'{olia_uri}Adjective')
        add_unique_triple(graph, sub, RDF.type, obj)
        return
    if (pos.lower() == "substantiv"):
        sub = URIRef(f'http://container1:8080/wictionary/resource/Noun/{get_resource_key("Noun")}')                    
        obj = URIRef(f'{olia_uri}Noun')
        add_unique_triple(graph, sub, RDF.type, obj)
        return

dump = mwxml.Dump.from_file(open(f'{os.path.expanduser("~")}/MyData/wiktionary/dewiktionary-20231101-pages-meta-current.xml'))
graph = Graph()
resource_cntr = defaultdict(int)
for page in dump:
    lemma = page.title
    id = page.id 
    form = {}
    pos = None
    for revision in page:        
        
        wikitext = revision.text        
        parsed_wikicode = mwparserfromhell.parse(wikitext)
        templates = parsed_wikicode.filter_templates()
        lang = get_template(templates, "sprache")
        if lang and lang.get(1).lower() == "deutsch":
            wortart_template = get_template(templates, "wortart")
            pos = wortart_template.get("1").value
            form_template = get_template_contains(templates, f"Deutsch {pos} Übersicht")
            if form_template and pos.lower() in allowed_pos:
                form = params_to_dict(form_template.params)            
                    
        if lemma and pos and pos.lower() in allowed_pos:
            add_triples(graph, lemma, pos, form)
            print(f"Lemma: {lemma}")
            print(f"POS: {pos}")            
            print(f"Form: {form}")
            print("\n---\n")

        lemma = None
        pos = None
        form = {}    