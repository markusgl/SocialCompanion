from unittest import TestCase

from analytics_engine.analytics import AnalyticsEngine, StanfordAnalyzer


class TestAnalyticsEngine(TestCase):
    def setUp(self):
        self.analytics = AnalyticsEngine()
        #self.text_analyzer = StanfordAnalyzer()

    def test_analyze_utterance(self):
        self.analytics.analyze_utterance(u'Hans und sein Sohn Hubert.')

