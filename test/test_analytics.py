from unittest import TestCase

from analytics_engine.analytics import AnalyticsEngine, LANG


class TestAnalyticsEngine(TestCase):
    def setUp(self):
        self.analytics = AnalyticsEngine(lang=LANG.DE)

    def test_analyze_utterance(self):
        result = self.analytics.analyze_utterance(u'Hans und sein Sohn Hubert.')

