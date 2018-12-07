import spacy
import os

from abc import ABC, abstractmethod
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from knowledge_graph.knowledge_graph import KnowledgeGraph
from network_core.network_graph import NetworkGraph
from analytics_engine import models
from spacy import displacy
from analytics_engine.relationship_extraction import RelationshipExtractor

java_path = "C:/Program Files/Java/jdk1.8.0_181/bin/java.exe"
os.environ['JAVAHOME'] = java_path

relationship_list = ['vater', 'mutter', 'sohn', 'tochter', 'bruder', 'schwester', 'enkel', 'enkelin', 'nichte',
                     'neffe', 'onkel', 'tante']


class AnalyticsEngine:
    def __init__(self):
        #self.text_analyzer = StanfordAnalyzer()
        #self.kg = KnowledgeGraph()
        self.ng = NetworkGraph()  # neo4j
        self.re = RelationshipExtractor()

    def analyze_utterance(self, utterance):
        relation_tuples = self.re.extract_relation_tuples(utterance)

        for relation_tuple in relation_tuples:

            ent1 = relation_tuple[0][0]
            ent2 = relation_tuple[2][0]
            rel = relation_tuple[1][0]

            # add entites to neo4j
            self.ng.add_relationship(ent1, ent2, rel_type=rel)

        # TODO extract relationship type
        # TODO generate response

        #response = "Ich habe Sie leider nicht verstanden."


        #return response


if __name__ == '__main__':
    ae = AnalyticsEngine()
    ae.analyze_utterance(u'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.')


class TextAnalyzer(ABC):

    @abstractmethod
    def extract_entities(self, utterance):
        pass

    def display_dependecies(self, utterance):
        SpacyAnalyzer().display_dependencies(utterance)


class SpacyAnalyzer(TextAnalyzer):
    def __init__(self):
        self.nlp = spacy.load('de_core_news_sm')

    def extract_entities(self, utterance):
        people = set()
        locations = set()

        doc = self.nlp(utterance)
        for ent in doc.ents:
            print("Entity: {}, Label: {}".format(ent, ent.label_))
            if ent.label_ == 'PER':
                people.add(ent.text)
            if ent.label_ == 'LOC':
                locations.add(ent.text)

        return people, locations

    def display_dependencies(self, utterance):
        doc = self.nlp(utterance)
        displacy.serve(doc, style='dep')

    def tag_pos(self, utterance):
        doc = self.nlp(utterance)
        nouns = []
        verbs = []
        for token in doc:
            if token.pos_ == 'VERB' and not token.is_stop:
                verbs.append(token)
            elif token.pos_ == 'NOUN':
                nouns.append(token)

        return nouns, verbs


class StanfordAnalyzer(TextAnalyzer):
    def __init__(self):
        model = 'models/dewac_175m_600.crf.ser.gz'
        #model = 'models/hgc_175m_600.crf.ser.gz'
        self.st = StanfordNERTagger(model,
                                    'models/stanford-ner.jar',
                                    encoding='utf-8')

    def extract_entities(self, utterance):
        people = set()
        locations = set()
        tokenized_text = word_tokenize(utterance)
        classified = self.st.tag(tokenized_text)

        for entity in classified:
            entity_text = entity[0]
            entity_label = entity[1]
            print("Entity: {}, Label: {}".format(entity_text, entity_label))
            if entity_label == 'I-PER':
                people.add(entity_text)
            elif entity_label == 'I-LOC':
                locations.add(entity_text)

        return people, locations


