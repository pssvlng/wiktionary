import os
import mwxml
import mwparserfromhell


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

dump = mwxml.Dump.from_file(open(f'{os.path.expanduser("~")}/MyData/wiktionary/dewiktionary-20231101-pages-meta-current.xml'))
for page in dump:
    lemma = page.title
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
            print(f"Lemma: {lemma}")
            print(f"POS: {pos}")
            if pos.lower() == 'adverb':
                pass
            print(f"Form: {form}")
            print("\n---\n")

        lemma = None
        pos = None
        form = {}    