""" Approach using NLTK and a predefined grammar based on ReVerb System (Fader et al. 2011)
* run POS tagger and entity chunker over each sentence
* for every verb chunk, find the nearest noun chunk to the left and the right of the verb
"""

import de_core_news_sm
import nltk

from nltk.tokenize import sent_tokenize
from network_core.ogm.node_objects import Me, Contact

class RelationshipExtractor:
    RELATIONSHIPS = ['vater', 'mutter', 'sohn', 'tochter', 'bruder', 'schwester', 'enkel', 'enkelin', 'nichte',
                         'neffe', 'onkel', 'tante']
    ME = ['ich', 'meine', 'mein']

    def __init__(self):
        self.nlp = de_core_news_sm.load()

        # grammar for spaCy POS Tags
        # extracts noun phrases (NP) and relationships (REL)
        self.grammar = r"""NP: {<DET>?<ADJ>*<NOUN>?<PROPN|PRON>*}
                      V: {<VERB>}
                      W: {<NOUN|ADJ|ADV|PRON|DET>}
                      P: {<ADP|PART|PUNCT>}
                      C: {<CONJ>}
                      REL: {<V><W>*<P>|<V><P>|<V>|<C>}
                      """

    def pos_tagging(self, utterance):
        pos_tagged_sentences = []
        sentences = sent_tokenize(utterance)

        for sentence in sentences:
            doc = self.nlp(sentence)

            pos_tagged_sentence = []
            for token in doc:
                pos_tuple = (token.text, token.pos_)
                pos_tagged_sentence.append(pos_tuple)

            pos_tagged_sentences.append(pos_tagged_sentence)

        return pos_tagged_sentences

    def extract_chunk_trees(self, utterance):
        sentence_trees = []
        cp = nltk.RegexpParser(self.grammar)

        pos_tagged_sentences = self.pos_tagging(utterance)

        for sentence in pos_tagged_sentences:
            sentence_trees.append(cp.parse(sentence))

        return sentence_trees

    def find_nearest_noun_chunk(self, rel_tree_position, sent_tree):
        """
        finds the nearest noun chunk left or right from the relationship tree
        :param rel_tree_position: position of the relationship tree in the sentence
        :param sent_tree: nltk tree of the current sentence
        :return:
        """
        i = rel_tree_position
        left_np = None
        right_np = None

        # find the nearest NP to the left of REL
        for j in range(i - 1, -1, -1):
            if type(sent_tree[j]) is nltk.tree.Tree and sent_tree[j].label() == 'NP':
                left_np = sent_tree[j]
                break
        # find the nearest NP to the right of REL
        for j in range(i + 1, len(sent_tree), 1):
            if type(sent_tree[j]) is nltk.tree.Tree and sent_tree[j].label() == 'NP':
                right_np= sent_tree[j]
                break

        return left_np, right_np

    def find_relations_tree_in_utterance(self, utterance):
        sentence_trees = self.extract_chunk_trees(utterance)

        relations = []
        for sent_tree in sentence_trees:
            for i, sub_tree in enumerate(sent_tree):
                if type(sub_tree) is nltk.tree.Tree and sub_tree.label() == 'REL':
                    rel = sub_tree

                    # find the nearest NP to the left of REL
                    left_np, right_np = self.find_nearest_noun_chunk(i, sent_tree)

                    relations.append([left_np, rel, right_np])

        return relations


    def extract_relation_tuples(self, utterance):

        relations = self.find_relations_tree_in_utterance(utterance)

        relation_tuples = []
        for i, relation in enumerate(relations):
            ne1_tree = relation[0]
            ne2_tree = relation[2]
            rel_tree = relation[1]

            # search for PROPN - if not found search for NOUN
            ne1 = [w for w, t in ne1_tree.leaves() if t == 'PROPN']
            if not ne1:
                ne1 = [w for w, t in ne1_tree.leaves() if t == 'NOUN']

            # search for PROPN - if not found search for NOUN
            ne2 = [w for w, t in ne2_tree.leaves() if t == 'PROPN']
            if not ne2:
                ne2 = [w for w, t in ne2_tree.leaves() if t == 'NOUN']

                # search for VERB - if not found search for CONJ
            rel = [w for w, t in rel_tree.leaves() if t == 'VERB']
            if not rel:
                rel = [w for w, t in rel_tree.leaves() if t == 'CONJ']

            if ne1 and ne2 and rel:
                relation_tuples.append((ne1, rel, ne2))

        return relation_tuples

    def print_relationships(self, utterance):
        relation_tuples = self.extract_relation_tuples(utterance)

        # convert relation tuples to objects
        for relation in relation_tuples:
            print(relation)

