import os
import spacy
#from nltk.corpus import tiger
from rdflib import Graph


from rdflib import Graph

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

graph = Graph()
ttl_file_path = f'{os.path.expanduser("~")}/MyData/dbnary/de_dbnary_morphology.ttl'
batched_parse(graph, ttl_file_path)



def func2(doc):
    for token in doc:
            print(
                f"{token.text}({token.lemma_}) - {token.pos_}: {str(token.morph)}"
            )
def func1(doc):
    for token in doc:
        if token.pos_ == "VERB":
            # Extract verb features
            mood = token.morph.get("Mood", "Unknown")
            person = token.morph.get("Person", "Unknown")
            voice = token.morph.get("Voice", "Unknown")
            tense = token.morph.get("Tense", "Unknown")

            # Print information about the verb
            print(
                f"{token.text} - {token.pos_}: Mood={mood}, Person={person}, Voice={voice}, Tense={tense}"
            )
        else:
            case = None
            number = None
            pronoun = False

            # Identify grammatical case
            if token.dep_ == "dat" or token.dep_ == "iobj":
                case = "dative"
            elif token.dep_ == "acc" or token.dep_ == "dobj":
                case = "accusative"
            elif token.dep_ == "gen":
                case = "genitive"
            elif token.dep_ == "nom" or (token.pos_ == "PRON" and token.dep_ == "nsubj"):
                case = "nominative"

            # Identify number (singular or plural)
            if "Number=Sing" in token.tag_:
                number = "singular"
            elif "Number=Plur" in token.tag_:
                number = "plural"

            # Check if it's a pronoun
            if token.pos_ == "PRON":
                pronoun = True

            # Print information
            print(
                f"{token.text} - {token.pos_}: Case={case}, Number={number}, Pronoun={pronoun}"
            )    

    print("\n" + "=" * 40 + "\n")






# with open('file1.txt', 'r', encoding='utf-8') as file:    
#    file_content = file.readlines()

# sentences = tiger.sents()
# nlp = spacy.load("de_core_news_sm")

# print(" ".join(file_content))
# sentence_str = " ".join(file_content)
# doc = nlp(sentence_str)
# func2(doc)


