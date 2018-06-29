from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import urllib.request

from neo4j.exceptions import ServiceUnavailable
from rasa_core.agent import Agent
from rasa_core.channels import HttpInputChannel
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.channels.telegram import TelegramInput
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies import MemoizationPolicy, KerasPolicy
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   BinarySingleStateFeaturizer)

from interpreter_luis import Interpreter
#from interpreter_dialogflow import Interpreter
from knowledge_base.knowledge_graph import KnowledgeGraph

logger = logging.getLogger(__name__)


def train_bot():
    logging.basicConfig(level='INFO')

    training_data_file = './data/stories'
    model_path = './models/dialogue'

    fallback = FallbackPolicy(fallback_action_name="utter_not_understood",
                              core_threshold=0.3, nlu_threshold=0.6)
    featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(), max_history=5)
    agent = Agent('./data/domain.yml', policies=[MemoizationPolicy(max_history=5), KerasPolicy(featurizer), fallback])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            augmentation_factor=50,
            epochs=500,
            batch_size=10,
            validation_split=0.2)

    agent.persist(model_path)


def run_cli_bot(serve_forever=True, train=False):
    logging.basicConfig(level="INFO")
    try:
        KnowledgeGraph()
    except ServiceUnavailable:
        print('Neo4j connection failed. Program stopped.')
        return

    if train:
        train_bot()
    interpreter = Interpreter()
    agent = Agent.load('./models/dialogue', interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
        
    return agent


def run_telegram_bot(webhook_url, train=False):
    logging.basicConfig(level="INFO")
    try:
        KnowledgeGraph()
    except ServiceUnavailable:
        print('Neo4j connection failed. Program stopped.')
        return

    if train:
        train_bot()

    with open('keys.json') as f:
        data = json.load(f)
    telegram_api_key = data['telegram-api-key']

    # set webhook of telegram bot
    try:
        telegram_url = 'https://api.telegram.org/bot' + telegram_api_key + '/setWebhook?url=' + webhook_url
        urllib.request.urlopen(telegram_url)
    except:
        print("Error setting telegram webhook")
        return

    interpreter = Interpreter()
    agent = Agent.load('./models/dialogue', interpreter)

    input_channel = (TelegramInput(access_token=telegram_api_key,
                                   verify='event123_bot',
                                   webhook_url=webhook_url,
                                   debug_mode=True))

    agent.handle_channel(HttpInputChannel(5004, '/app', input_channel))


if __name__ == '__main__':
    #run_cli_bot(train=True)
    run_telegram_bot('423b0d06.ngrok.io/app/webhook', True)
