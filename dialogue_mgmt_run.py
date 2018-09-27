from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import urllib.request
import os
import enum

from neo4j.exceptions import ServiceUnavailable
from rasa_core.agent import Agent
from rasa_core.channels import HttpInputChannel
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.channels.telegram import TelegramInput
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies import MemoizationPolicy, KerasPolicy
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   BinarySingleStateFeaturizer)
from interpreter_luis import Interpreter as LuisInterpreter
from interpreter_dialogflow import Interpreter as DialogflowInterpreter
from interpreter_witai import Interpreter as WitInterpreter
from network_graph.network_graph import NetworkGraph
from speech_handling.text_to_speech import TextToSpeech

logger = logging.getLogger(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class NLU(enum.Enum):
    dialogflow = 1
    luis = 2
    rasanlu = 3
    witai = 4


def train_bot():
    logging.basicConfig(level='INFO')

    training_data_file = './data/stories'
    model_path = './models/dialogue'
    domain_file = './data/domain.yml'

    # core_threshold: min confidence needed to accept an action prediction from Rasa Core
    # nlu_threshold: min confidence needed to accept an NLU prediction
    fallback = FallbackPolicy(fallback_action_name="utter_not_understood",
                              core_threshold=0.5,
                              nlu_threshold=0.4)

    featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(), max_history=3)
    agent = Agent(domain=domain_file,
                  policies=[MemoizationPolicy(max_history=2),
                            KerasPolicy(featurizer), fallback])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            augmentation_factor=50,
            epochs=400,
            batch_size=50,
            validation_split=0.2)

    agent.persist(model_path)


def run_cli_bot(serve_forever=True, train=False, nlu_name=None):
    logging.basicConfig(level="INFO")

    try:
        NetworkGraph()
    except ServiceUnavailable:
        logging.info('Neo4j connection failed. Program stopped.')
        return

    if train:
        train_bot()

    interpreter = select_interpreter(nlu_name)
    if not interpreter:
        return ("Please provide one of these interpreters: luis, dialogflow, witai, rasa")

    agent = Agent.load('./models/dialogue', interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
        
    return agent


def run_telegram_bot(webhook_url, train=False, nlu_name=None, bot_name=None):
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
        logging.info('Neo4j connection successful.')
    except ServiceUnavailable as service_err:
        logging.error('Neo4j connection failed. Program stopped: {}'.format(service_err))
        return

    # set webhook of telegram bot
    try:
        logging.info("Setting Telegram webhook to {}".format(webhook_url))
        telegram_url = 'https://api.telegram.org/bot' + telegram_api_key + '/setWebhook?url=' + webhook_url + \
                       '&max_connections=1' + 'allowed_updates=[message]'
        urllib.request.urlopen(telegram_url)
    except Exception as err:
        logging.error("Error setting Telegram webhook: {}".format(err))
        return

    # Set Interpreter (NLU) to given engine
    interpreter = select_interpreter(nlu_name)
    if not interpreter:
        # set Interpreter to Dialogflow if connection is possible and no interpreter was given
        if DialogflowInterpreter().check_connection():
            interpreter = DialogflowInterpreter()
            logging.info("Interpreter (NLU) set to Dialogflow.")
        # set Interpreter to RASA NLU if no connection to Dialoflow is possible and none explicitly given
        else:
            interpreter = 'rasa-nlu/models/rasa-nlu/default/socialcompanionnlu'
            logging.info("Interpreter (NLU) set to Rasa NLU.")

    agent = Agent.load('./models/dialogue', interpreter)
    logging.info('Agent model loaded.')

    # set TTS runtime to Google if available otherwise use Windows local SAPI engine
    gtts_available = TextToSpeech().check_google_connection()
    if gtts_available:
        TextToSpeech.runtime = 'google'
        logging.info("Setting TTS to Google TTS")
    else:
        TextToSpeech.runtime = 'sapi'
        logging.info("Setting TTS to Microsoft Speech Engine")

    logging.info('Starting Telegram channel...')
    try:
        input_channel = (TelegramInput(access_token=telegram_api_key,
                                       verify=bot_name,
                                       webhook_url=webhook_url,
                                       debug_mode=True))
        agent.handle_channel(HttpInputChannel(5004, '/app', input_channel))
    except Exception as err:
        logging.error("Error starting Telegram Channel: {}".format(err))


def select_interpreter(nlu_name):
    if nlu_name == NLU.luis:
        interpreter = LuisInterpreter()
    elif nlu_name == NLU.dialogflow:
        interpreter = DialogflowInterpreter()
    elif nlu_name == NLU.witai:
        interpreter = WitInterpreter()
    elif nlu_name == NLU.rasanlu:
        interpreter = 'rasa-nlu/models/rasa-nlu/default/socialcompanionnlu'
    else:
        return None

    return interpreter


if __name__ == '__main__':
    keys_file = 'dm_config.json'
    with open(keys_file) as f:
        config = json.load(f)
    webhook = config['telegram_webhook']
    bot_name = config['telegram-bot-name']

    run_telegram_bot(webhook_url=webhook, train=False, nlu_name="blub", bot_name=bot_name)
    #run_cli_bot(train=False, interpreter='rasa')

