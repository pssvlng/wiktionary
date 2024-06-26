import wn
import sys
import tempfile
import os
from passivlingo_dictionary.encoders.WordEncoder import WordEncoder
from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper
from pathlib import Path
from .ImageWrapper import getArgvTransform, getFontName
from .ImageWrapper import writeOutput
from .ImageWrapper import formatNodeDisplay


def main(argv):

    try:

        argvTransform = getArgvTransform(argv)

        dotFilePath = os.path.sep.join(
            [tempfile.gettempdir(), f"{argvTransform['fileName']}.dot"])
        pngFilePath = os.path.sep.join(
            [tempfile.gettempdir(), f"{argvTransform['fileName']}.png"])
        data = {"result": True, "filePath": pngFilePath, "msg": "Success"}

        if Path(pngFilePath).is_file():
            print(WordEncoder().encode(data))
            return

        synset_to_wrap = wn.synset(argvTransform['synsetId'])
        synset = OwnSynsetWrapper(synset_to_wrap.lexicon().language, synset_to_wrap)
        level = int(argvTransform['level'])
        branch_count = int(argvTransform['maxLeafNodes'])
        filter_langs = argvTransform['filterLangs']
        ili = argvTransform['ili']
        synonym_count = int(argvTransform['synonymCount'])
        lemma = argvTransform['lemma']

        body = f'{buildgraph_body(synset, level, filter_langs, ili, synonym_count, branch_count, True, lemma)}{buildgraph_body(synset, level, filter_langs, ili, synonym_count, branch_count, False, lemma)}'
        partwhole_template = '''strict digraph g {
            rankdir=RL            
            "{root0}" [fontname={font_name0} shape=box, style=bold]
            node [fontname={font_name0} shape = box,height=.1];
            {body}
        }'''

        root = formatNodeDisplay(synset, filter_langs, ili, synonym_count, lemma)
        font_name = getFontName(filter_langs)
        writeOutput(partwhole_template, root, body,
                    font_name, dotFilePath, pngFilePath, data)

    except Exception as e:
        repr_ = getattr(e, 'message', repr(e))
        str_ = getattr(e, 'message', str(e))
        data = {"result": False, "filePath": pngFilePath,
                "msg": f'repr: {repr_}, str: {str_}'}
        print(WordEncoder().encode(data))


def buildgraph_body(synset, level, filter_langs, ili, synonym_count, branch_count, build_up, lemma, edge_label=''):
    if level == 0:
        return ''

    if build_up:
        branches = synset.holonyms()
    else:
        branches = synset.meronyms()

    root = formatNodeDisplay(synset, filter_langs, ili, synonym_count, lemma)
    entry = ''
    returnstr = ''
    for item in branches[:branch_count]:
        itemDisplay = formatNodeDisplay(
            item, filter_langs, item.ili, synonym_count, item.lemmas()[0])
        if build_up:
            entry = f'{entry}"{root}"->"{itemDisplay}" [label="{edge_label}"][dir=back];'
        else:
            entry = f'{entry}"{itemDisplay}"->"{root}" [label="{edge_label}"][dir=back];'

        returnstr = f'{returnstr}{buildgraph_body(item, level-1, filter_langs, item.ili, synonym_count, branch_count, build_up, item.lemmas()[0], edge_label)}'

    return f'{entry}{returnstr}'


if __name__ == "__main__":
    main(sys.argv[1:])
