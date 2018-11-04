from unittest import TestCase

from analytics_engine.analytics import AnalyticsEngine, StanfordAnalyzer


class TestAnalyticsEngine(TestCase):
    def setUp(self):
        self.analytics = AnalyticsEngine()
        self.text_analyzer = StanfordAnalyzer()

    def test_analyze_utterance(self):
        self.analytics.analyze_utterance(u'Mein Name ist Hans. '
                                         u'Und meine Schwester heißt Ursula.')

    def test_extract_person_entity(self):
        names = self.text_analyzer.extract_entities(u'Mein Name ist Hans.')
        assert names.pop() == 'Hans'
