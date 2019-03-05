"""
Patter based relation extraction
"""

import logging
import re
import nltk
import en_core_web_md
import de_core_news_sm

from nltk.tokenize import word_tokenize

from analytics_engine.flair_embeddings import FlairEmbeddingModels
from analytics_engine.relation_types import RelationTypes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PatternBasedRE:
    def __init__(self, nlp=None, grammar=None, relationship_list=None, me_list=None, embeddings_model=None):
        self.nlp = nlp
        self.grammar = grammar
        self.relationship_list = relationship_list
        self.me_list = me_list
        self.relation_types = RelationTypes()
        self.embeddings_model = embeddings_model

    @classmethod
    def de_lang(cls):
        nlp = de_core_news_sm.load()
        embeddings_model = FlairEmbeddingModels().de_lang()
        # PP: e.g. 'I habe einen Sohn', 'I habe einen kleinen Bruder'
        # NP: e.g. 'Meine kleine Schwester'
        grammar = r"""
                PP: {<PRON><AUX><DET><ADJ>?<NOUN>}
                NP: {<DET><ADJ>?<NOUN>}            
                REL: {<PP>|<NP>}"""
        relationship_list = ['vater', 'mutter', 'sohn', 'tochter', 'bruder', 'schwester', 'enkel', 'enkelin',
                             'großvater', 'großmutter', 'ehemann', 'ehefrau', 'onkel', 'tante', 'freund']
        me_list = ['ich', 'mein', 'meine']

        return cls(nlp, grammar, relationship_list, me_list, embeddings_model)

    @classmethod
    def en_lang(cls):
        nlp = en_core_web_md.load()
        embeddings_model = FlairEmbeddingModels().en_lang()
        # PP: e.g. 'I have a son', 'I have a smaller brother', 'I have a 9 year old son'
        # NP: e.g. 'My (little) sister'
        grammar = r"""
                    PP: {<PRON><VERB><NUM>?<DET>?<ADJ>?<NOUN>}
                    NP: {<ADJ><ADJ>?<NOUN>}            
                    REL: {<PP>|<NP>}"""
        relationship_list = ['father', 'mother', 'sister', 'brother', 'son', 'daughter', 'husband', 'wife',
                             'grandson', 'granddaughter', 'grandmother', 'grandfather', 'uncle', 'aunt', 'friend']
        me_list = ['i', 'my', 'me']

        return cls(nlp, grammar, relationship_list, me_list, embeddings_model)

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

    def __measure_relation_similarity(self, rel_tree_words):
        """
        Measures the cosine similarity between word embeddings
        :param rel_tree_words: dict of sp values
        :return: relation type with the highest score
        """
        relation = None
        highest_score = 0
        highest_rel = None
        threshold = 0.6

        for rel in self.relationship_list:
            try:
                # get word embeddings representation of extracted relation and relation
                score = self.embeddings_model.n_similarity(rel_tree_words, [rel])
                logger.debug(f'{rel} {score}')
                if score > highest_score:
                    highest_score = score
                    highest_rel = rel
            except KeyError as err:
                logger.debug(err)

        if highest_score > threshold:
            logger.debug(f'Highest score for {rel_tree_words} - {highest_rel}, Score: {highest_score}')
            relation = self.relation_types.get_relation_type(highest_rel)

        return relation

    def extract_rel(self, sentence, plot_tree=False):
        extracted_relations = []

        # build chunks
        chunk_tree = self.chunk_sentence(self.pos_tag_sentence(sentence), draw=plot_tree)

        for i, sub_tree in enumerate(chunk_tree):
            if type(sub_tree) is nltk.tree.Tree and sub_tree.label() == 'REL':
                me = sub_tree[0][0][0].lower()
                rel_tree_words = []
                for word in sub_tree[0]:
                    if word[0] not in self.me_list:
                        rel_tree_words.append(word[0])

                if me in self.me_list and rel_tree_words:
                    relation_type = self.__measure_relation_similarity(rel_tree_words)

                    if sub_tree[0][-1][1] == 'PROPN':
                        rel_person = sub_tree[0][-1][0]
                        extracted_relation = rel_person, relation_type, 'USER'
                        extracted_relations.append(extracted_relation)
                    else:
                        extracted_relation = relation_type, 'USER'
                        extracted_relations.append(extracted_relation)

        return extracted_relations


if __name__ == '__main__':
    text1 = ''''my dad flies airplanes .'''
    text2 = ''' That's what my mom said.'''
    pbre = PatternBasedRE().en_lang()
    rel = pbre.extract_rel(text2)
    print(rel)
