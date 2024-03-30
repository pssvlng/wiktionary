import os
import wn
from passivlingo_dictionary.encoders.WordEncoder import WordEncoder
from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper
from video_generation_consts import *


def getArgvTransform(argv):
    if len(argv) < 3:
        raise ValueError('Program expects at least 3 arguments')

    argvTransform = {
        'fileName': None,
        'level': None,
        'filterLangs': None,
        'maxLeafNodes': None,
        'ili': None,
        'synonymCount': None,
        'synsetId': None,        
        'hierarchy': False,
        'partWhole': False,
        'lemma': None
    }

    for item in argv:        
        argvTransform[item] = argv[item]

    return argvTransform


def getFontName(filterLangs):
    langs = filterLangs.split(',')

    if len(set(['zh', 'jp']) & set(langs)) > 0:
        return 'SimSun'

    if len(set(['arb', 'fas', 'fa', 'he']) & set(langs)) > 0:
        return '"DejaVu Sans"'

    if 'th' in langs:
        return '"Angsana New"'

    return 'Arial'


def writeOutput(template, root, body, font_name, dotFilePath, pngFilePath, result, body1=None, rankdir=None):
    fileText = template.replace('{font_name0}', font_name)
    fileText = fileText.replace('{root0}', root)
    fileText = fileText.replace('{body}', body)
    if not body1 is None:
        fileText = fileText.replace('{body1}', body1)
    if not rankdir is None:
        fileText = fileText.replace('{rankdir}', rankdir)

    with open(dotFilePath, 'w', encoding='utf-8') as file:
        file.write(fileText)

    os.system(f'dot -Tpng {dotFilePath} -o {pngFilePath}')
    print(WordEncoder().encode(result))


def formatSynonymDisplay(synset, synonym_count, lemma):
    lemmas = synset.lemmas()
    if lemma in lemmas:
        lemmas.remove(lemma)
        lemmas.insert(0, lemma)
    result = ''

    if synset.id != '*INFERRED*':
        result = lemmas[0]
        for synonym in lemmas[1:synonym_count]:
            result += f',{synonym}'
    
    return f'{result} [{pos_description_short[synset.lang][synset.pos]}]'


def formatNodeDisplay(synset, filter_langs, ili, synonym_count, lemma):

    result = {}
    if filter_langs and ili:
        langs = filter_langs.split(',')
        if 'en' in langs:
            langs.remove('en')
            langs.insert(0, 'en')
        for lang in langs:
            synsets_local = wn.synsets(ili=ili, lang=lang.strip())
            if len(synsets_local) > 0:
                s = OwnSynsetWrapper(synsets_local[0].lexicon().language, synsets_local[0])
                result[lang] = formatSynonymDisplay(s, synonym_count, lemma)
    else:
        result[synset.id] = formatSynonymDisplay(synset, synonym_count, lemma)

    if len(result) == 0:
        synset_to_wrap = wn.synsets(ili=ili, lang='en')[0]        
        s = OwnSynsetWrapper(synset_to_wrap.lexicon().language, synset_to_wrap)
        result['en'] = formatSynonymDisplay(s, synonym_count, lemma)

    return f"{'|'.join(result.values())}"
