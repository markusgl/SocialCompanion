import spacy
from unittest import TestCase
from analytics_engine.relation_extraction_dep_path import RelExtractorDepPath


class TestRelExtractorDep(TestCase):
    def setUp(self):
        self.rel_ex = RelExtractorDepPath()
        self.nlp = spacy.load('de')

    def test_named_entity_extraction(self):
        text = u'''Hans, welcher der Sohn von Hubert ist, geht mit Peter ins Kino.'''
        document = self.nlp(text)
        result = self.rel_ex.named_entity_extraction(document)
        print(result)
