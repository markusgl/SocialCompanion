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
from voice_input_channel import VoiceInput
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies import MemoizationPolicy, KerasPolicy
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   BinarySingleStateFeaturizer)

from interpreter_luis import Interpreter as LuisInterpreter
from interpreter_dialogflow import Interpreter as DialogflowInterpreter
from interpreter_witai import Interpreter as WitInterpreter
from rasa_nlu.model import Interpreter as RasaInterpreter

from knowledge_base.knowledge_graph import KnowledgeGraph
from speech_handling.speech_recognizer import SpeechHandler
logger = logging.getLogger(__name__)


def train_bot():
    logging.basicConfig(level='INFO')

    training_data_file = './data/stories'
    model_path = './models/dialogue'

    fallback = FallbackPolicy(fallback_action_name="utter_not_understood",
                              core_threshold=0.3, nlu_threshold=0.3)
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


def run_cli_bot(serve_forever=True, train=False, interpreter='luis'):
    logging.basicConfig(level="INFO")
    try:
        KnowledgeGraph()
    except ServiceUnavailable:
        print('Neo4j connection failed. Program stopped.')
        return

    if train:
        train_bot()

    if interpreter == 'luis':
        interpreter = LuisInterpreter()
    elif interpreter == 'dialogflow':
        interpreter = DialogflowInterpreter()
    elif interpreter == 'witai':
        interpreter = WitInterpreter()
    elif interpreter == 'rasa':
        interpreter = RasaInterpreter.load('rasa-nlu/models/rasa-nlu/default/socialcompanionnlu')
    else:
        return ("Please provide one of these interpreters: luis, dialogflow, witai, rasa")

    agent = Agent.load('./models/dialogue', interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
        
    return agent


def run_telegram_bot(webhook_url, train=False, interpreter='luis'):
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

    if interpreter == 'luis':
        interpreter = LuisInterpreter()
    elif interpreter == 'dialogflow':
        interpreter = DialogflowInterpreter()
    elif interpreter == 'witai':
        interpreter = WitInterpreter()
    elif interpreter == 'rasa':
        interpreter = RasaInterpreter.load('rasa-nlu/models/rasa-nlu/default/socialcompanionnlu')
    else:
        return ("Please provide one of these interpreters: luis, dialogflow, witai, rasa")

    agent = Agent.load('./models/dialogue', interpreter)

    input_channel = (TelegramInput(access_token=telegram_api_key,
                                   verify='SocialCompanionBot',
                                   webhook_url=webhook_url,
                                   debug_mode=True))

    agent.handle_channel(HttpInputChannel(5004, '/app', input_channel))


def run_voice_bot(webhook_url, train=False, interpreter='luis'):
    logging.basicConfig(level="INFO")
    try:
        KnowledgeGraph()
    except ServiceUnavailable:
        print('Neo4j connection failed. Program stopped.')
        return

    if train:
        train_bot()

    if interpreter == 'luis':
        interpreter = LuisInterpreter()
    elif interpreter == 'dialogflow':
        interpreter = DialogflowInterpreter()
    elif interpreter == 'witai':
        interpreter = WitInterpreter()
    elif interpreter == 'rasa':
        interpreter = RasaInterpreter.load('rasa-nlu/models/rasa-nlu/default/socialcompanionnlu')
    else:
        return ("Please provide one of these interpreters: luis, dialogflow, witai, rasa")

    agent = Agent.load('./models/dialogue', interpreter)

    input_channel = (VoiceInput(url='SocialCompanionBot'))
    agent.handle_channel(HttpInputChannel(5004, '/app', input_channel))

    """
    sr = SpeechHandler()
    message = sr.speech_to_text()
    print(message)
    if not message:
        agent.handle_message(message)
    """
    #print(agent.start_message_handling('Hallo'))
    #if serve_forever:
    #    agent.handle_message('Hallo')

    return agent

if __name__ == '__main__':
    #run_cli_bot(train=True, interpreter='rasa')
    #run_telegram_bot('3c956e75.ngrok.io/app/webhook', True, interpreter='luis')
    run_voice_bot('https://c89804d8.ngrok.io')

