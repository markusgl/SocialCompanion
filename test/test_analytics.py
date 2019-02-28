from unittest import TestCase

from analytics_engine.analytics import AnalyticsEngine
from analytics_engine.relation_extractor import LANG


class TestAnalyticsEngineGerman(TestCase):
    def setUp(self):
        self.ae = AnalyticsEngine(lang=LANG.DE)

    def test_analyze_utterance_1(self):
        result = self.ae.analyze_utterance(u'Hans und sein Sohn Hubert.')
        assert result == [('hubert', 'son-of', 'hans')]


class TestAnalyticsEngineEnglish(TestCase):
    def setUp(self):
        self.ae = AnalyticsEngine(lang=LANG.EN)

    def test_analyze_utterance_1(self):
        utterance = u'Peter is the father of Tom.'
        result = self.ae.analyze_utterance(utterance)
        assert result == [('peter', 'father-of', 'tom')]

    def test_analyze_utterance_2(self):
        utterance = u'My daughter Lisa is moving to London next month.'
        result = self.ae.analyze_utterance(utterance)
        assert result == [('lisa', 'daughter-of', 'USER')]

    # TODO fix
    def test_analyze_utterance_3(self):
        utterance = u'''Tom's sister Lisa lives in London now.'''
        result = self.ae.analyze_utterance(utterance)
        assert result == [('lisa', 'sister-of', 'tom')]

    def test_analyze_utterance_4(self):
        utterance = u'''Peter, Tom's father, will pick us up.'''
        result = self.ae.analyze_utterance(utterance)
        assert result == [('peter', 'father-of', 'tom')]

    def test_analyze_utterance_5(self):
        utterance = u'''my sister , madonna , does too .'''
        result = self.ae.analyze_utterance(utterance)
        assert result == [('madonna', 'sister-of', 'USER')]
