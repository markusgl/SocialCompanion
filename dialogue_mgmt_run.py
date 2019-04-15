from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import os
import enum
import argparse

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
from network_core.network_graph import NetworkGraph
from custom_channels.voice_channel import VoiceInput
from custom_channels.telegram_custom import TelegramCustomInput

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class NLU(enum.Enum):
    dialogflow = 1
    luis = 2
    rasanlu = 3
    witai = 4


def train_bot():
    training_data_file = './data/stories'
    model_path = './models/dialogue'
    domain_file = './data/domain.yml'

    # core_threshold: min confidence needed to accept an action predicted by Rasa Core
    # nlu_threshold: min confidence needed to accept an intent predicted by the interpreter (NLU)
    fallback = FallbackPolicy(fallback_action_name="action_not_understood",
                              core_threshold=0.5,
                              nlu_threshold=0.35)

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
    if not test_neo4j_connection():
        return

    if train:
        train_bot()

    interpreter = select_interpreter(nlu_name)
    agent = Agent.load('./models/dialogue', interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
        
    return agent


def run_telegram_bot(train=False, nlu_name=None, voice_output=False, url=None):
    webhook_url, bot_name, telegram_api_key = load_dm_config()

    if url:
        webhook_url = url + '/app/webhook'

    if train:
        train_bot()

    if not test_neo4j_connection():
        return

    # Set Interpreter (NLU) to th given engine
    interpreter = select_interpreter(nlu_name)

    # load the trained agent model
    agent = Agent.load('./models/dialogue', interpreter)
    logging.info('Agent model loaded.')

    logging.info('Starting Telegram channel...')
    try:
        if voice_output:
            input_channel = (TelegramCustomInput(access_token=telegram_api_key,
                                                 verify=bot_name,
                                                 webhook_url=webhook_url,
                                                 debug_mode=True))
        else:
            input_channel = (TelegramInput(access_token=telegram_api_key,
                                           verify=bot_name,
                                           webhook_url=webhook_url,
                                           debug_mode=True))
        agent.handle_channel(HttpInputChannel(5004, '/app', input_channel))
    except Exception as err:
        logging.error("Error starting Telegram Channel: {}".format(err))


def run_voice_channel(train=False, nlu_name=None, url=None):
    if train:
        train_bot()

    if url:
        webhook_url = url + '/app/webhook'

    interpreter = select_interpreter(nlu_name)
    agent = Agent.load('./models/dialogue', interpreter)
    input_channel = VoiceInput()
    agent.handle_channel(HttpInputChannel(5004, '/app', input_channel))


def test_neo4j_connection():
    try:
        NetworkGraph()
        logging.info('Neo4j connection successful.')
    except ServiceUnavailable as service_err:
        logging.error('Neo4j connection failed. Program stopped: {}'.format(service_err))
        return False

    return True


def select_interpreter(nlu_name):  # TODO use factory methods instead
    if nlu_name == NLU.luis:
        interpreter = LuisInterpreter()
    elif nlu_name == NLU.dialogflow:
        interpreter = DialogflowInterpreter()
    elif nlu_name == NLU.witai:
        interpreter = WitInterpreter()
    elif nlu_name == NLU.rasanlu:
        interpreter = 'rasa-nlu/models/rasa-nlu/default/socialcompanionnlu'
    else:
        # set Interpreter to Dialogflow if connection is possible and no interpreter was provided
        if DialogflowInterpreter().check_connection():
            interpreter = DialogflowInterpreter()
            logging.info("Interpreter (NLU) set automatically to Dialogflow because on interpeter was provided.")
        # set Interpreter to RASA NLU if no connection to Dialoflow is possible and none was explicitly provided
        else:
            interpreter = 'rasa-nlu/models/rasa-nlu/default/socialcompanionnlu'
            logging.info("Interpreter (NLU) set automatically to Rasa NLU because on interpeter was provided.")

    return interpreter


def load_dm_config():
    keys_file = 'dm_config.json'
    with open(keys_file) as f:
        config = json.load(f)
    webhook = config['telegram_webhook']
    bot_name = config['telegram-bot-name']
    api_key = config['telegram-api-key']

    return webhook, bot_name, api_key


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, help="https web hook url from ngrok")
    parser.add_argument("--tts", type=bool, help="if true, text to speech output is activated")
    parser.add_argument("--train", type=bool, help="if true, (re-)trains the dialog model")
    parser.add_argument("--voicechannel", type=bool, help="if true, runs the voice channel")
    parser.add_argument("--cli", type=bool, help="if true, runs the cli channel")
    args = parser.parse_args()

    if args.url and args.tts and args.train:
        run_telegram_bot(train=args.train, nlu_name=NLU.rasanlu, voice_output=args.tts, url=args.url)
    elif args.url and args.train:
        run_telegram_bot(train=args.train, nlu_name=NLU.rasanlu, voice_output=False, url=args.url)
    elif args.url and args.tts:
        run_telegram_bot(train=False, nlu_name=NLU.rasanlu, voice_output=args.tts, url=args.url)
    elif args.url:
        run_telegram_bot(train=False, nlu_name=NLU.rasanlu, voice_output=False, url=args.url)
    elif args.voicechannel and args.url:
        run_voice_channel(train=False, nlu_name=NLU.rasanlu, url=args.url)
    elif args.cli:
        run_cli_bot(train=False, nlu_name=NLU.rasanlu)
    else:
        run_telegram_bot(train=False, nlu_name=NLU.rasanlu, voice_output=False)


