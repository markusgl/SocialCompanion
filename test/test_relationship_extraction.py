from unittest import TestCase
from analytics_engine.relationship_extraction import RelationshipExtractor


class TestRelationshipExtractor(TestCase):

    def setUp(self):
        self.rel_ex = RelationshipExtractor()

    def test_find_relationships(self):
        test_utterance = u'''Peter und Maria gehen morgen ins Kino.'''

        rel = self.rel_ex.print_relationships(test_utterance)
        self.assertEqual(rel[0][0][0], 'Peter')
        self.assertEqual(rel[0][2][0], 'Maria')

