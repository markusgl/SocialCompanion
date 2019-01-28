''' NER Taggers '''

import re
import en_core_web_md

from abc import ABC, abstractmethod
from nltk.tokenize import word_tokenize
from flair.data import Sentence
from flair.models import SequenceTagger


class EntityExtractor(ABC):

    @abstractmethod
    def extract_entities(self, utterance):
        pass


class SpacyEntityExtractor(EntityExtractor):
    def __init__(self):
        self.nlp = en_core_web_md.load()
        self.spacy_per_symbol = 'PERSON'
        self.me_list = ['i', 'my']

    def extract_entities(self, raw_text):
        """
        extracts PER-PER and USER-PER entities
        :param raw_text:
        :return: list of found entities
        """
        sentence = re.sub('\s{2,}', ' ', raw_text)  # delete multiple consecutive spaces
        doc = self.nlp(sentence)
        entities = []

        for token in doc:
            if token.text.lower() in self.me_list:
                entities.append('USER')

        for ent in doc.ents:
            if ent.label_ == self.spacy_per_symbol:
                entities.append(ent.text.lower())

        return entities


class FlairEntityExtractor(EntityExtractor):
    def __init__(self):
        self.flair_tagger = SequenceTagger.load('de-ner')
        self.me_list = ['ich', 'mein', 'meine']

    def __extract_pronoun_entities(self, text):
        entities = []
        for token in word_tokenize(text):
            if token.lower() in self.me_list:
                entities.append('USER')

        return entities

    def extract_entities(self, raw_text):
        entities = self.__extract_pronoun_entities(raw_text)
        #raw_text = re.sub(r'\W+', ' ', raw_text)  # delete non word characters
        raw_text = re.sub('\s{2,}', ' ', raw_text)  # delete multiple consecutive spaces

        sentence = Sentence(raw_text)  # instantiate sentence object
        self.flair_tagger.predict(sentence)

        # NER Spans
        for entity in sentence.get_spans('ner'):
            if entity.tag == 'PER':
                if len(entity.tokens) > 1:
                    entities.append(str(entity.text.lower()).replace(' ', '_'))
                else:
                    entities.append(entity.text.lower())

        return entities
