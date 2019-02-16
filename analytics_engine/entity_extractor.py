"""
Different NER Tagger implementations within one abstract class
Used for extracting only PERSON entities and PRONOUNS for social relation extraction
 * spaCy NER Tagger (English)
 * Flair NER Tagger (German)
 * Stanford NER Tagger (English)
"""

import re
import os
import en_core_web_md

from abc import ABC, abstractmethod

from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger

from flair.data import Sentence
from flair.models import SequenceTagger


class EntityExtractor(ABC):
    @abstractmethod
    def extract_entities(self, utterance):
        pass


class FlairEntityExtractor(EntityExtractor):
    def __init__(self, flair_tagger=None, me_list=None):
        self.flair_tagger = flair_tagger
        self.me_list = me_list

    # Factory methods for language selection
    @classmethod
    def de_lang(cls):
        flair_tagger = SequenceTagger.load('de-ner')
        me_list = ['ich', 'mein', 'meine']
        return cls(flair_tagger, me_list)

    @classmethod
    def en_lang(cls):
        flair_tagger = SequenceTagger.load('ner')
        me_list = ['i', 'my']
        return cls(flair_tagger, me_list)

    def __extract_pronoun_entities(self, text):
        entities = []
        for token in word_tokenize(text):
            if token.lower() in self.me_list:
                entities.append('USER')

        return entities

    def extract_entities(self, raw_text):
        """
        Extracts PERSON entities and pronouns defined in me_list
        :param raw_text: raw utterance
        :return: list of entities
        """
        #entities = self.__extract_pronoun_entities(raw_text)
        raw_text = re.sub(r'\W+', ' ', raw_text)  # delete non word characters
        raw_text = re.sub('\s{2,}', ' ', raw_text)  # delete multiple consecutive spaces
        per_entities = []
        entities = []

        sentence = Sentence(raw_text, use_tokenizer=True)  # instantiate sentence object
        self.flair_tagger.predict(sentence)

        for token in sentence:
            entity_tag = token.get_tag('ner')
            entity_name = token.text.lower()

            # TODO handle multiple word entities
            # Person entities 'PER'
            if entity_tag.value == 'S-PER' or entity_tag.value == 'I-PER' or entity_tag.value == 'B-PER' or entity_tag.value == 'E-PER':
                entities.append(entity_name)
                per_entities.append(entity_name)
            # Personal pronoun entities 'USR'
            elif entity_name in self.me_list:
                entities.append(entity_name)

        # NER Spans
        """
        for entity in sentence.get_spans('ner'):
            if entity.tag == 'PER':
                if len(entity.tokens) > 1:
                    entities.append(str(entity.text.lower()).replace(' ', '_'))
                else:
                    entity_name = re.sub(r"'s?", '', entity.text.lower())
                    entities.append(entity_name)
                    per_entities.append(entity_name)
            elif entity.text.lower() in self.me_list:
                entity_name = re.sub(r"'s?", '', entity.text.lower())
                entities.append(entity_name)
        """

        return entities, per_entities


class SpacyEntityExtractor(EntityExtractor):
    def __init__(self):
        self.nlp = en_core_web_md.load()
        self.spacy_per_symbol = 'PERSON'
        self.me_list = ['i', 'my']

    def extract_entities(self, raw_text):
        """
        FOR ENGLISH TEXTS
        Extracts PERSON enties and pronouns defined in me_list
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


class StanfordAnalyzer(EntityExtractor):
    def __init__(self):
        java_path = "C:/Program Files/Java/jdk1.8.0_181/bin/java.exe"
        os.environ['JAVAHOME'] = java_path

        # choose a model
        model = 'models/dewac_175m_600.crf.ser.gz'
        #model = 'models/hgc_175m_600.crf.ser.gz'
        self.st = StanfordNERTagger(model,
                                    'models/stanford-ner.jar',
                                    encoding='utf-8')

        self.me_list = ['i', 'my']

    def extract_entities(self, raw_text):
        """
        FOR ENGLISH TEXTS
        Extracts PERSON enties and pronouns defined in me_list
        :param raw_text:
        :return: list of entities
        """
        entities = []
        raw_text = re.sub('\s{2,}', ' ', raw_text)  # delete multiple consecutive spaces
        tokenized_text = word_tokenize(raw_text)
        classified = self.st.tag(tokenized_text)

        for entity in classified:
            entity_text = entity[0]
            entity_label = entity[1]

            if entity_text in self.me_list or entity_label == 'I-PER':
                entities.append(entity_text)

        return entities
