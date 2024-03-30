title_page = {}
title_page['en'] = "{LEMMAS} is a {POS} in English, and it means {DEFINITION}."
title_page['de'] = "{LEMMAS} ist ein {POS} in {LANG}, und es bedeutet {DEFINITION}."
title_page['nl'] = "{LEMMAS} is een {POS} in {LANG}, en het betekent {DEFINITION}."

synonyms = {}
synonyms['en'] = "Synonyms"
synonyms['de'] = "Synonyme"
synonyms['nl'] = "Synoniemen"

synonym_text = {}
synonym_text['en'] = "Synonyms for {LEMMA} include: {SYNONYMS}"
synonym_text['de'] = "Synonyme für {LEMMA} sind: {SYNONYMS}"
synonym_text['nl'] = "Synoniemen voor {LEMMA} zijn onder meer: {SYNONYMS}"

example = {}
example['en'] = "An example sentence: {SENTENCE}"
example['de'] = "Ein Beispielsatz: {SENTENCE}"
example['nl'] = "Een voorbeeldzin: {SENTENCE}"

hypernym_text = {}
hypernym_text['en'] = "Word(s) with a related, but more general, meaning of the English {POS} '{LEMMAS}' are '{HYPERNYMS}'."
hypernym_text['de'] = "Wort(e) mit einer verwandten, aber allgemeineren Bedeutung des deutschen {POS}s '{LEMMAS}' sind '{HYPERNYMS}'."
hypernym_text['nl'] = "Woorden met een verwante, maar algemenere betekenis van het Nederlandse {POS} '{LEMMAS}' zijn '{HYPERNYMS}'."

hyponym_text = {}
hyponym_text['en'] = "Word(s) with a related, but more specific, meaning of the English {POS} '{LEMMAS}' are '{HYPONYMS}'."
hyponym_text['de'] = "Wort(e) mit einer verwandten, aber spezifischeren Bedeutung des deutschen {POS}s '{LEMMAS}' sind '{HYPONYMS}'."
hyponym_text['nl'] = "Woorden met een verwante, maar meer specifieke betekenis van het Nederlandse {POS} '{LEMMAS}' zijn '{HYPONYMS}'."

meronym_text = {}
meronym_text['en'] = "Word(s) that form part of the English {POS} '{LEMMAS}' are '{MERONYMS}'."
meronym_text['de'] = "Wort(e), die Teil des deutschen {POS}s '{LEMMAS}' sind, sind '{MERONYMS}'."
meronym_text['nl'] = "Woorden die deel uitmaken van het Nederlandse"

holonym_text = {}
holonym_text['en'] = "The English {POS} '{LEMMAS}' is part of the word(s) '{HOLONYMS}'."
holonym_text['de'] = "Das deutsche {POS} '{LEMMAS}' ist Teil des/der Wortes/Wörter '{HOLONYMS}'."
holonym_text['nl'] = "Het Nederlandse {POS} '{LEMMAS}' maakt deel uit van het woord (de woorden) '{HOLONYMS}'."

prompt_instruction = {}
prompt_instruction['en'] = "Write a short, explanatory text to explain the linguistic relationship between the {POS} '{LEMMAS}' and the aforementioned relationships it has with other words."
prompt_instruction['de'] = "Schreiben Sie einen kurzen erklärenden Text, um die sprachliche Beziehung zwischen dem {POS} '{LEMMAS}' und den oben genannten Beziehungen zu anderen Wörtern zu erläutern."
prompt_instruction['nl'] = "Schrijf een korte verklarende tekst om de taalkundige relatie uit te leggen tussen het {POS} '{LEMMAS}' en de eerder genoemde relaties die het heeft met andere woorden."

lang_description = {}
lang_description['en'] = "English"
lang_description['de'] = "Deutsch"
lang_description['nl'] = "Nederlands"

pos_description = {}
pos_description['en'] = {}
pos_description['en']['n'] = "noun"
pos_description['en']['v'] = "verb"
pos_description['en']['a'] = "adjective"
pos_description['en']['s'] = "adjective"
pos_description['en']['r'] = "adverb"

pos_description['de'] = {}
pos_description['de']['n'] = "Substantiv"
pos_description['de']['v'] = "Verb"
pos_description['de']['a'] = "Adjectiv"
pos_description['de']['s'] = "Adjectiv"
pos_description['de']['r'] = "Adverb"

pos_description['nl'] = {}
pos_description['nl']['n'] = "zelfstandige Naamwoord"
pos_description['nl']['v'] = "werkwoord"
pos_description['nl']['a'] = "byvoeglijke Naamwoord"
pos_description['nl']['s'] = "byvoeglijke Naamwoord"
pos_description['nl']['r'] = "bijwoord"

pos_description_short = {}
pos_description_short['en'] = {}
pos_description_short['en']['n'] = "n."
pos_description_short['en']['v'] = "v."
pos_description_short['en']['a'] = "adj."
pos_description_short['en']['s'] = "adj."
pos_description_short['en']['r'] = "adv."

pos_description_short['de'] = {}
pos_description_short['de']['n'] = "Sub."
pos_description_short['de']['v'] = "V."
pos_description_short['de']['a'] = "Adj."
pos_description_short['de']['s'] = "Adj."
pos_description_short['de']['r'] = "Adv."

pos_description_short['nl'] = {}
pos_description_short['nl']['n'] = "z.nw."
pos_description_short['nl']['v'] = "ww."
pos_description_short['nl']['a'] = "b.nw."
pos_description_short['nl']['s'] = "b.nw"
pos_description_short['nl']['r'] = "bw."
