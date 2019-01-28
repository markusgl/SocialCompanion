from unittest import TestCase
from analytics_engine.old.relation_extraction_verb import RelationshipExtractor


class TestRelationshipExtractor(TestCase):

    def setUp(self):
        self.rel_ex = RelationshipExtractor()

    def test_find_relationships_single_sentence(self):
        text = u'''Peter und Maria gehen morgen ins Kino.'''

        rel = self.rel_ex.extract_relation_tuples(text)
        self.assertEqual(rel[0][0][0], 'Peter')
        self.assertEqual(rel[0][2][0], 'Maria')

    def test_find_relationship_with_multiple_sentences(self):
        text = u'Hubert ist der Vater von Hans. Peter und Michael gehen ins Kino. ' \
               u'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'
        rel = self.rel_ex.extract_relation_tuples(text)
        self.assertEqual(rel[0][0][0], 'Peter')
        self.assertEqual(rel[0][2][0], 'Michael')
        self.assertEqual(rel[1][2][0], 'Kino')
        self.assertEqual(rel[2][2][0], 'Lukas')
