from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from neo4j.exceptions import ServiceUnavailable
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.policies import FallbackPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from interpreter_luis import Interpreter
#from interpreter_dialogflow import Interpreter
from knowledge_base.knowledge_graph import KnowledgeGraph

logger = logging.getLogger(__name__)


def run_eventbot_online(input_channel, interpreter,
                        domain_file="./data/domain.yml",
                        training_data_file='./data/stories'):
    try:
        KnowledgeGraph()
    except ServiceUnavailable:
        print('Neo4j connection failed. Program stopped.')
        return

    fallback = FallbackPolicy(fallback_action_name="utter_not_understood",
                              core_threshold=0.3, nlu_threshold=0.6)
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy(), fallback],
                  interpreter=interpreter)

    data = agent.load_data(training_data_file)
    agent.train_online(data,
                       input_channel=input_channel,
                       max_history=2,
                       batch_size=50,
                       epochs=200,
                       max_training_samples=300)

    return agent


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    luis_interpreter = Interpreter()
    run_eventbot_online(ConsoleInputChannel(), luis_interpreter)
