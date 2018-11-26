
from analytics_engine.analytics import AnalyticsEngine


class ActionBaseClass:
    def __init__(self):
        self.ae = AnalyticsEngine()

    def analyze_utterance(self, utterance):
        self.ae.analyze_utterance(utterance)
