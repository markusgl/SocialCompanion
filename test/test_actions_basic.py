from unittest import TestCase

from rasa_core.dispatcher import Dispatcher
from rasa_core.domain import Domain
from rasa_core.trackers import DialogueStateTracker

from actions_basic import ActionNotUnderstood, ActionUtterGreet
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel, ConsoleOutputChannel


class TestActionNotUnderstood(TestCase):
    def setUp(self):
        self.not_undestood = ActionNotUnderstood()
        # set Interpreter (NLU) to Rasa NLU
        self.interpreter = 'rasa-nlu/models/rasa-nlu/default/socialcompanionnlu'

        # load the trained agent model
        self.agent = Agent.load('./models/dialogue', self.interpreter)
        self.agent.handle_channel(ConsoleInputChannel())

        # TODO mock dispatcher, tracker and domain
        self.dispatcher = Dispatcher(output_channel=ConsoleOutputChannel())
        self.tracker = DialogueStateTracker()
        self.domain = Domain()

    #def test_utter_not_understood(self):
        # TODO
     #   self.not_undestood.run()


class TestActionUtterGreet(TestCase):
    def setUp(self):
        self.action_utter_greet = ActionUtterGreet()

    def test_analyze_utterance(self):
        self.action_utter_greet.analyze_utterance('Hans ist der Vater von Hubert.')

