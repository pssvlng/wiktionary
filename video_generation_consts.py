TITLE_PAGE_EN = """
{LEMMAS} is a {POS} in {LANG}, and it means {DEFINITION}. 
"""
SYNONYM_TEXT_EN = """
Synonyms for {LEMMA} include: {SYNONYMS}
"""

TITLE_PAGE_DE = """
{LEMMAS} ist ein {POS} in {LANG}, und es bedeutet {DEFINITION}. 
"""

SYNONYM_TEXT_DE = """
Synonyme für {LEMMA} sind: {SYNONYMS}
"""

TITLE_PAGE_NL = """
{LEMMAS} is een {POS} in {LANG}, en het betekent {DEFINITION}. 
"""

SYNONYM_TEXT_NL = """
Synoniemen voor {LEMMA} zijn onder meer: {SYNONYMS}
"""

EXAMPLE_TEXT_EN = """
An example sentence: {SENTENCE}
"""

EXAMPLE_TEXT_DE = """
Ein Beispielsatz: {SENTENCE}
"""

EXAMPLE_TEXT_NL = """
Een voorbeeldzin: {SENTENCE}
"""

def get_example_text(lang):
    if lang == 'en':
        return EXAMPLE_TEXT_EN
    if lang == 'nl':
        return EXAMPLE_TEXT_NL
    if lang == 'de':
        return EXAMPLE_TEXT_DE

def get_synonym_text(lang):
    if lang == 'en':
        return SYNONYM_TEXT_EN
    if lang == 'nl':
        return SYNONYM_TEXT_NL
    if lang == 'de':
        return SYNONYM_TEXT_DE

def get_title_page_text(lang):
    if lang == 'en':
        return TITLE_PAGE_EN
    if lang == 'nl':
        return TITLE_PAGE_NL
    if lang == 'de':
        return TITLE_PAGE_DE
    
def get_pos_en(pos):
    if pos == 'n':
        return 'noun'
    if pos == 'v':
        return 'verb'
    if pos in ['a', 's']:
        return 'adjective'
    if pos == 'r':
        return 'adverb'
    
def get_pos_de(pos):
    if pos == 'n':
        return 'Substantiv'
    if pos == 'v':
        return 'Verb'
    if pos in ['a', 's']:
        return 'Adjectiv'
    if pos == 'r':
        return 'Adverb'    

def get_pos_nl(pos):
    if pos == 'n':
        return 'Selfstandige Naamwoord'
    if pos == 'v':
        return 'Werkwoord'
    if pos in ['a', 's']:
        return 'Byvoeglijke Naamwoord'
    if pos == 'r':
        return 'Bijwoord'        

def get_pos(pos, lang):
    if lang == 'en':
        return get_pos_en(pos)
    if lang == 'nl':
        return get_pos_nl(pos)
    if lang == 'de':
        return get_pos_de(pos)

def get_full_lang(lang):
    if lang == 'en':
        return 'English'
    if lang == 'de':
        return 'Deutsch'
    if lang == 'nl':
        return 'Nederlands'    