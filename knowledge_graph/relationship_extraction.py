import spacy
import nltk

from nltk.tokenize import sent_tokenize


class RelationshipExtractor:
    def __init__(self):
        self.nlp = spacy.load('de')

        # grammar for spaCy POS Tags
        # extracts noun phrases (NP) and relationships (REL)
        self.grammar = r"""NP: {<DT>?<JJ>*<PROPN|NOUN|PRON>}
                      V: {<VERB>}
                      W: {<NOUN|ADJ|ADV|PROPN|DET>}
                      P: {<ADP|PART|PUNCT>}
                      C: {<CONJ>}
                      REL: {<V><W>*<P>|<V><P>|<V>|<C>}
                      """

    def pos_tagging(self, sentences):
        pos_tagged_sentences = []

        for sentence in sentences:
            doc = self.nlp(sentence)

            pos_tagged_sentence = []
            for token in doc:
                pos_tuple = (token.text, token.pos_)
                pos_tagged_sentence.append(pos_tuple)

            pos_tagged_sentences.append(pos_tagged_sentence)

        return pos_tagged_sentences

    def extract_chunk_trees(self, pos_tagged_sentences):
        sentence_trees = []
        cp = nltk.RegexpParser(self.grammar)

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

    def find_relationships(self, utterance):
        relations = []

        sentences = sent_tokenize(utterance)
        pos_tagged_sentences = self.pos_tagging(sentences)
        sentence_trees = self.extract_chunk_trees(pos_tagged_sentences)

        for sent_tree in sentence_trees:
            for i, sub_tree in enumerate(sent_tree):
                if type(sub_tree) is nltk.tree.Tree and sub_tree.label() == 'REL':
                    rel = sub_tree

                    # find the nearest NP to the left of REL
                    left_np, right_np = self.find_nearest_noun_chunk(i, sent_tree)

                    relations.append([left_np, rel, right_np])

        relation_tuples = []
        for relation in relations:
            relation_tuple = []
            for tree in relation:
                words = [w for w, t in tree.leaves()]
                relation_tuple.append(tuple(words))

            relation_tuples.append(relation_tuple)

        return relation_tuples

