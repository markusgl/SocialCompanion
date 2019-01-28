'''
Build flair embeddings
'''

import re

from flair.data import Sentence
from flair.embeddings import WordEmbeddings
from torch import nn


class FlairEmbeddings:
    def __init__(self):
        self.glove_embedding = WordEmbeddings('de')
        # self.glove_embedding = WordEmbeddings('de-crawl')  # FastText embeddings
        self.flair_embeddings = {}

    def get_word_embeddings(self, text):
        """
        get the glove word embdding representation of multiple words
        :param text: array of words as strings
        :return: sum of word embeddings inside text
        """
        text = re.sub(r'\s{2,}', ' ', text)
        sentence = Sentence(text)
        self.glove_embedding.embed(sentence)

        words_embeddings = []
        for token in sentence:
            words_embeddings.append(token.embedding)

        return sum(words_embeddings)

    def n_similarity(self, words1, words2):
        """
        cosine similarity betwee words1 and words2
        :param words1: array of words as strings
        :param words2: array of words as strings
        :return: cosine similarity between the two word arrays
        """
        text1 = ''
        for word in words1:
            text1 += word + ' '

        text2 = ''
        for word in words2:
            text2 += word + ' '

        words1_embeddings = self.get_word_embeddings(text1)
        words2_embeddings = self.get_word_embeddings(text2)

        # measure cosine similarity between both embedding summaries
        cos = nn.CosineSimilarity(dim=0)
        result = cos(words1_embeddings, words2_embeddings)

        return result