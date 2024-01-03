from nltk.corpus import wordnet as wn
from rdflib import Namespace

lexvo = {}
lexvo['en'] = 'http://www.lexvo.org/page/iso639-3/eng'
lexvo['de'] = 'http://www.lexvo.org/page/iso639-3/deu'

nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
dbpedia = Namespace("http://dbpedia.org/resource/")
itsrdf = Namespace("http://www.w3.org/2005/11/its/rdf#")
curriculum_ns = Namespace("https://w3id.org/curriculum/")
ili_uri = "http://ili.globalwordnet.org/ili/"
ili_en_uri = "https://en-word.net/ttl/ili/"
olia_uri = "http://purl.org/olia/olia.owl#"
olia_ns = Namespace("http://purl.org/olia/olia.owl#")
oersi_ns = Namespace("https://edu.yovisto.com/resource/oersi#")


def add_unique_triple(g, subject, predicate, object):
    if (subject, predicate, object) not in g:
        g.add((subject, predicate, object))

    return g    