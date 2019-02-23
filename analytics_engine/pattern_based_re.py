"""
Patter based relation extraction
"""

import re
import nltk
import en_core_web_md
import de_core_news_sm

from nltk.tokenize import word_tokenize

from analytics_engine.relation_types import RelationTypes


class PatternBasedRE:
    def __init__(self, nlp=None, grammar=None, relationship_list=None, me_list=None):
        self.nlp = nlp
        self.grammar = grammar
        self.relationship_list = relationship_list
        self.me_list = me_list
        self.relation_types = RelationTypes()

    @classmethod
    def de_lang(cls):
        nlp = de_core_news_sm.load()
        # PP: e.g. 'I habe einen Sohn', 'I habe einen kleinen Bruder'
        # NP: e.g. 'Meine kleine Schwester'
        grammar = r"""
                PP: {<PRON><AUX><DET><ADJ>?<NOUN>}
                NP: {<DET><ADJ>?<NOUN>}            
                REL: {<PP>|<NP>}"""
        relationship_list = ['vater', 'mutter', 'papa', 'papi', 'mama', 'mami', 'sohn', 'tochter', 'bruder',
                                  'schwester', 'enkel', 'enkelin', 'nichte', 'neffe', 'großvater', 'großmutter', 'opa',
                                  'oma', 'onkel', 'tante', 'cousin', 'cousine', 'schwager', 'schwägerin', 'mann',
                                  'frau', 'ehemann', 'ehefrau']
        me_list = ['ich', 'mein', 'meine']

        return cls(nlp, grammar, relationship_list, me_list)

    @classmethod
    def en_lang(cls):
        nlp = en_core_web_md.load()
        # PP: e.g. 'I have a son', 'I have a smaller brother', 'I have a 9 year old son'
        # NP: e.g. 'My (little) sister'
        grammar = r"""
                    PP: {<PRON><VERB><NUM>?<DET>?<ADJ>?<NOUN>}
                    NP: {<ADJ><ADJ>?<NOUN>}            
                    REL: {<PP>|<NP>}"""
        relationship_list = ['father', 'mother', 'dad', 'daddy', 'mom', 'son', 'daughter', 'brother', 'sister',
                             'grandchild', 'grandson', 'granddaughter', 'grandfather', 'grandmother',
                             'niece', 'nephew', 'uncle', 'aunt', 'cousin', 'husband', 'wife']
        me_list = ['i', 'my']

        return cls(nlp, grammar, relationship_list, me_list)


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
        chunk_tree = cp.parse(pos_tagged_sentence)

        if draw:
            chunk_tree.draw()

        return chunk_tree

    def extract_rel(self, sentence, plot_tree=False):
        extracted_relations = []

        # build chunks
        chunk_tree = self.chunk_sentence(self.pos_tag_sentence(sentence), draw=plot_tree)

        for i, sub_tree in enumerate(chunk_tree):
            if type(sub_tree) is nltk.tree.Tree and sub_tree.label() == 'REL':
                me = sub_tree[0][0][0].lower()
                rel = [word for word in sub_tree[0] if word[0].lower() in self.relationship_list]

                if me in self.me_list and rel:
                    relation = [item for item in rel[0]]
                    relation_type = self.relation_types.get_relation_type(relation[0])

                    if sub_tree[0][-1][1] == 'PROPN':
                        rel_person = sub_tree[0][-1][0]
                        extracted_relation = rel_person, relation_type, 'USER'
                        extracted_relations.append(extracted_relation)
                    else:
                        extracted_relation = relation_type, 'USER'
                        extracted_relations.append(extracted_relation)

        return extracted_relations

