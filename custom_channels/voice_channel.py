from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json

from flask import Blueprint, request, jsonify
from rasa_core import utils
from rasa_core.channels.channel import UserMessage, OutputChannel
from rasa_core.channels.rest import HttpInputComponent

from speech_handling.text_to_speech import SapiTTS, GoogleTTS

from frontend.qt_gui import ChatWindow
from PyQt5.QtWidgets import *

logger = logging.getLogger(__name__)


class VoiceOutput(OutputChannel):
    """A bot that uses a custom channel to communicate."""

    def __init__(self, url=None):
        self.url = url
        self.tts = GoogleTTS()
        self.default_output_color = utils.bcolors.OKBLUE
        self.chat_window = ChatWindow()

    def send_text_message(self, recipient_id, message):
        print(f'Sending text message to output: {message}')
        # send to Qt GUI
        # TODO
        self.chat_window.connect.appendMessage('message')

        # cmd output
        utils.print_color(message, self.default_output_color)

        # send response message via http
        url = self.url
        data = {"sender": "bot", "message": message}

        data_json = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        requests.post(
                url=url,
                data=data_json,
                headers=headers
        )

        return self.tts.utter_voice_message(message)


class VoiceInput(HttpInputComponent):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "voice"

    def __init__(self, output_url=None):
        self.out_channel = VoiceOutput(output_url)

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)
        out_channel = self.out_channel

        @custom_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/message", methods=['POST'])
        def message():
            payload = request.json
            print(f"Payload received: {payload}")

            sender_id = payload.get("sender", None)
            text = payload.get("message", None)
            try:
                if text == '/start':
                    on_new_message(UserMessage('/start', out_channel,
                                               sender_id))
                else:
                    on_new_message(UserMessage(text, out_channel, sender_id))
            except Exception as ex:
                logger.error(f'Exception trying to handle mesage: {ex}')

            return "success"

        return custom_webhook
