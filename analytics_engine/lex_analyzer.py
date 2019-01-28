## LexAnalyzer based on ReVerb (Etzioni et al. 2008)

import spacy
import re
import nltk
import enum
import en_core_web_md
import de_core_news_sm

from nltk.tokenize import word_tokenize


class LANG(enum.Enum):
    DE = 'de'
    EN = 'en'


class LexAnalyzer:
    def __init__(self, lang):
        if lang == 'de':
            self.nlp = de_core_news_sm.load()
            self.grammar = r"""
                    PP: {<PRON><AUX><DET><ADJ>?<NOUN>}
                    NP: {<DET><ADJ>?<NOUN><PROPN>*}            
                    REL: {<PP>|<NP>}"""

            self.relationship_list = ['vater', 'mutter', 'papa', 'papi', 'mama', 'mami', 'sohn', 'tochter', 'bruder',
                                 'schwester', 'enkel', 'enkelin', 'nichte', 'neffe', 'großvater', 'großmutter', 'opa',
                                 'oma', 'onkel', 'tante', 'cousin', 'cousine', 'schwager', 'schwägerin', 'mann', 'frau',
                                 'ehemann', 'ehefrau']
            self.me_list = ['ich', 'mein', 'meine']
        else:
            self.nlp = en_core_web_md.load()
            # PP: e.g. 'I have a son', 'I have a smaller brother', 'I have a 9 year old son'
            # NP: e.g. 'My (little) sister (Lisa)'
            self.grammar = r"""
                        PP: {<PRON><VERB><DET><ADJ>?<NOUN>}
                        NP: {<ADJ><ADJ>?<NOUN><PROPN>*}            
                        REL: {<PP>|<NP>}"""

            self.relationship_list = ['father', 'mother', 'dad', 'daddy', 'mom', 'son', 'daughter', 'brother', 'sister',
                                 'grandchild', 'grandson', 'granddaughter', 'grandfather', 'grandmother',
                                 'niece', 'nephew', 'uncle', 'aunt', 'cousin', 'husband', 'wife']
            self.me_list = ['i', 'my']

    def search_rel_type(self, sentence):
        for token in word_tokenize(sentence):
            if token.lower() in self.relationship_list:
                return token.lower()

        return None

    def pos_tag_sentence(self, sentence):
        sentence = re.sub('\W+', ' ', sentence)
        doc = self.nlp(sentence)

        pos_tagged_sentence = []
        for token in doc:
            pos_tuple = (token.text, token.pos_)
            pos_tagged_sentence.append(pos_tuple)

        return pos_tagged_sentence

    def chunk_sentence(self, pos_tagged_sentence, draw=False):
        cp = nltk.RegexpParser(self.grammar)
        result = cp.parse(pos_tagged_sentence)

        if draw:
            result.draw()

        return result

    def extract_rel(self, sentence):
        extracted_relations = []

        # build chunks
        chunk_tree = self.chunk_sentence(self.pos_tag_sentence(sentence))

        for i, sub_tree in enumerate(chunk_tree):
            if type(sub_tree) is nltk.tree.Tree and sub_tree.label() == 'REL':
                me = sub_tree[0][0][0].lower()
                rel = [word for word in sub_tree[0] if word[0] in self.relationship_list]
                if me in self.me_list and rel:
                    relation = [item for item in rel[0]]

                    if sub_tree[0][-1][1] == 'PROPN':
                        rel_person = sub_tree[0][-1][0]
                        extracted_relations.append(f'<USER, {relation[0]}, {rel_person}>')
                    else:
                        extracted_relations.append(f'<USER, {relation[0]}>')

        return extracted_relations
