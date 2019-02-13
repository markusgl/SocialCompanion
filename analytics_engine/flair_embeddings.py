"""
Handle Flair embeddings
(https://github.com/zalandoresearch/flair/blob/master/resources/docs/TUTORIAL_3_WORD_EMBEDDING.md)
"""

import re

from flair.data import Sentence
from flair.embeddings import WordEmbeddings, FlairEmbeddings, BertEmbeddings
from torch import nn


class FlairEmbeddingModels:
    def __init__(self, embeddings=None):
        self.embeddings = embeddings
        self.flair_embeddings = {}

    @classmethod
    def de_lang(cls):
        """
        Factory method for german embeddings
        """
        embeddings = WordEmbeddings('de')  # German FastText embeddings
        # embeddings = WordEmbeddings('de-crawl')  # German FastText embeddings trained over crawls
        #embeddings = BertEmbeddings('bert-base-multilingual-cased')

        return cls(embeddings)

    @classmethod
    def en_lang(cls):
        """
        Factory method for english embeddings
        """
        #embeddings = WordEmbeddings('en-glove')
        embeddings = WordEmbeddings('en-crawl')  # FastText embeddings over web crawls
        #embeddings = WordEmbeddings('en-news')
        #embeddings = FlairEmbeddings('news-forward')
        #embeddings = BertEmbeddings()

        return cls(embeddings)

    def get_word_embeddings(self, text):
        """
        get the glove word embdding representation of multiple words
        :param text: array of words as strings
        :return: sum of word embeddings inside text
        """
        text = re.sub(r'\s{2,}', ' ', text)
        sentence = Sentence(text)
        self.embeddings.embed(sentence)

        words_embeddings = []
        for token in sentence:
            words_embeddings.append(token.embedding)

        return sum(words_embeddings)

    def n_similarity(self, words1, words2):
        """
        Returns cosine similarity between words1 and words2 as a float (i.e. '100.0' means identical)
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

        # measure cosine similarity between both embedding summaries (tensors)
        cos = nn.CosineSimilarity(dim=0)
        result = cos(words1_embeddings, words2_embeddings)

        return result
