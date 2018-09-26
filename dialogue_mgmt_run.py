from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import urllib.request
import requests

from neo4j.exceptions import ServiceUnavailable
from rasa_core.agent import Agent
from rasa_core.events import AllSlotsReset
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
from rasa_core.events import ReminderScheduled

from network_graph.network_graph import NetworkGraph
from speech_handling.speech_to_text import SpeechHandler
import datetime
import os

logger = logging.getLogger(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def train_bot():
    logging.basicConfig(level='INFO')

    training_data_file = './data/stories'
    model_path = './models/dialogue'
    domain_file = './data/domain.yml'

    # core_threshold: min confidence needed to accept an action prediction from Rasa Core
    # nlu_threshold: min confidence needed to accept an NLU prediction
    fallback = FallbackPolicy(fallback_action_name="utter_not_understood",
                              core_threshold=0.5,
                              nlu_threshold=0.5)

    #featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(), max_history=3)
    agent = Agent(domain=domain_file,
                  policies=[MemoizationPolicy(max_history=2),
                            KerasPolicy(), fallback])
    """    
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy(), fallback])
    """
    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            augmentation_factor=50,
            epochs=400,
            batch_size=50,
            validation_split=0.2)

    agent.persist(model_path)


def run_cli_bot(serve_forever=True, train=False, interpreter='rasa'):
    logging.basicConfig(level="INFO")

    try:
        NetworkGraph()
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
        interpreter ='rasa-nlu/models/rasa-nlu/default/socialcompanionnlu'
    else:
        return ("Please provide one of these interpreters: luis, dialogflow, witai, rasa")

    agent = Agent.load('./models/dialogue', interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
        
    return agent


def run_telegram_bot(webhook_url, train=False, interpreter=None):
    logging.basicConfig(level="INFO")

    if train:
        train_bot()

    # read configuration from file
    with open(str(ROOT_DIR + '/keys.json')) as f:
        data = json.load(f)
    telegram_api_key = data['telegram-api-key']

    # test neo4j connection
    try:
        NetworkGraph()
        print('Neo4j connection successful.')
    except ServiceUnavailable:
        print('Neo4j connection failed. Program stopped.')
        return

    # set webhook of telegram bot
    try:
        print("setting webhook")
        telegram_url = 'https://api.telegram.org/bot' + telegram_api_key + '/setWebhook?url=' + webhook_url
        urllib.request.urlopen(telegram_url)
    except:
        print("Error setting Telegram webhook")
        return

    # Set Interpreter (NLU)
    if interpreter:
        if interpreter == 'luis':
            interpreter = LuisInterpreter()
        elif interpreter == 'dialogflow':
            interpreter = DialogflowInterpreter()
        elif interpreter == 'witai':
            interpreter = WitInterpreter()
        elif interpreter == 'rasa':
            interpreter = 'rasa-nlu/models/rasa-nlu/default/socialcompanionnlu'
    # set interpreter to dialogflow if connection is possible
    elif DialogflowInterpreter().check_connection():
        interpreter = DialogflowInterpreter()
        print("Interpreter set to Dialogflow.")
    # set interpreter to rasa nlu if no connection to dialoflow is possible
    else:
        interpreter = 'rasa-nlu/models/rasa-nlu/default/socialcompanionnlu'
        print("Interpreter set to Rasa NLU.")

    agent = Agent.load('./models/dialogue', interpreter)
    print('Agent loaded.')

    # set TTS runtime to sapi or google tts depending on internet connection
    # test internet connection
    try:
        requests.get("https://cloud.google.com/")
        tts_engine = 'google'
    except:
        tts_engine = 'sapi'

    with open('speech_handling/tts_config.json', 'r+') as jsonFile:
        data = json.load(jsonFile)
        tmp = data['engine']
        data['runtime'] = tts_engine

        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile)
        jsonFile.truncate()

    #trigger_date = datetime.datetime.strptime('2018-09-08 20:20', '%Y-%m-%d %H:%M')
    #ReminderScheduled('action_remind_drink', trigger_date.isoformat())

    print('Starting Telegram Channel...')
    input_channel = (TelegramInput(access_token=telegram_api_key,
                                   verify='careina1234_bot',
                                   webhook_url=webhook_url,
                                   debug_mode=False))

    agent.handle_channel(HttpInputChannel(5004, '/app', input_channel))


if __name__ == '__main__':
    #keys_file = 'dm_config.json'
    #with open(keys_file) as f:
    #    config = json.load(f)
    #webhook = config['telegram_webhook']

    webhook = 'https://9ce352ac.ngrok.io/app/webhook'
    run_telegram_bot(webhook, train=False, interpreter='rasa')
    #run_cli_bot(train=False, interpreter='rasa')

