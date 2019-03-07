from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests

from flask import Blueprint, request, jsonify
from rasa_core.channels.channel import UserMessage, OutputChannel
from rasa_core.channels.rest import HttpInputComponent
from rasa_core import utils

from speech_handling.text_to_speech import SapiTTS, GoogleTTS

logger = logging.getLogger(__name__)


class VoiceOutput(OutputChannel):
    """A bot that uses a custom channel to communicate."""

    def __init__(self, url, access_token):
        self.access_token = access_token
        self.url = url
        self.tts = SapiTTS()

    def send_text_message(self, recipient_id, message):
        self.tts.utter_voice_message(message)

        # you probably use http to send a message
        # For Google tts - TODO
        """
        url = self.url

        print(f'Response message: {message}')
        print(f'Response URL: {url}')
        if self.access_token is not None:
            headers = {"Auth-token": self.access_token}
        else:
            headers = {}

        requests.post(
                url,
                message,
                headers=headers
        )
        """


class VoiceInput(HttpInputComponent):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "voice"

    def __init__(self, url, access_token=None):
        self.out_channel = VoiceOutput(url, access_token)

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)
        out_channel = VoiceOutput(url='http://localhost:5000', access_token=None)

        @custom_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/message", methods=['POST'])
        def message():
            payload = request.json
            print(f"Payload received: {payload}")
            sender_id = payload.get("sender", None)
            text = payload.get("message", None)

            on_new_message(UserMessage(text, out_channel, sender_id))

            return "success"

        return custom_webhook
