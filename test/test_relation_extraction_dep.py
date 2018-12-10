from unittest import TestCase
from analytics_engine.relation_extraction_dep import RelExtractorDep

class TestRelExtractorDep(TestCase):
    def setUp(self):
        self.rel_ex = RelExtractorDep()

    def test_extract_relationship_with_multiple_sentences(self):
        text = u'Hubert ist der Vater von Hans. Peter und Michael gehen ins Kino.'' \
        '       'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'
        self.rel_ex.extract_relation_tuples(text)
