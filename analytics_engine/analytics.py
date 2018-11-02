import spacy
import os

from abc import ABC, abstractmethod
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from knowledge_graph.knowledge_graph import KnowledgeGraph
from analytics_engine import models

java_path = "C:/Program Files/Java/jdk1.8.0_181/bin/java.exe"
os.environ['JAVAHOME'] = java_path


class AnalyticsEngine:
    def __init__(self):
        self.text_analyzer = StanfordAnalyzer()
        self.kg = KnowledgeGraph()

    def analyze_utterance(self, utterance):
        names = self.text_analyzer.extract_person_entity(utterance)
        response = "Ich habe Sie leider nicht verstanden."

        # add names to knowledge graph
        if len(names) > 0:
            response = "Wer ist: "
            for name in names:
                self.kg.add_person(_given_name=name)
                response += name + " "

        return response


class TextAnalyzer(ABC):
    @abstractmethod
    def extract_person_entity(self, utterance):
        pass


class SpacyAnalyzer(TextAnalyzer):
    def extract_person_entity(self, utterance):
        people = set()

        nlp = spacy.load('de_core_news_sm')
        doc = nlp(utterance)
        for ent in doc.ents:
            if ent.label_ == 'PER':
                people.add(ent.text)

        return people


class StanfordAnalyzer(TextAnalyzer):
    def __init__(self):
        self.st = StanfordNERTagger('models/dewac_175m_600.crf.ser.gz',
                                    'models/stanford-ner.jar',
                                    encoding='utf-8')

    def extract_person_entity(self, utterance):
        people = set()

        tokenized_text = word_tokenize(utterance)
        classified = self.st.tag(tokenized_text)

        for entity in classified:
            if entity[1] == 'I-PER':
                people.add(entity[0])

        return people


class StanfordAnalyzer2(TextAnalyzer):
    def __init__(self):
        self.st = StanfordNERTagger('models/hgc_175m_600.crf.ser.gz',
                                    'models/stanford-ner.jar',
                                    encoding='utf-8')

    def extract_person_entity(self, utterance):
        people = set()

        tokenized_text = word_tokenize(utterance)
        classified = self.st.tag(tokenized_text)

        for entity in classified:
            if entity[1] == 'I-PER':
                people.add(entity[0])

        return people


if __name__ == '__main__':
    analyzer = StanfordAnalyzer()
    print(analyzer.extract_person_entity(u'Mein Name ist Hans.'))
