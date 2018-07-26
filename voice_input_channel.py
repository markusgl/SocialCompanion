from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging, json

from flask import Blueprint, request, jsonify
import requests
from rasa_core.channels.channel import UserMessage, OutputChannel
from rasa_core.channels.rest import HttpInputComponent
from rasa_core import utils

logger = logging.getLogger(__name__)


class VoiceOutput(OutputChannel):
    """A bot that uses a custom channel to communicate."""

    def __init__(self, url, access_token):
        self.access_token = access_token
        self.url = url
        self.default_output_color = utils.bcolors.OKBLUE

    def send_text_message(self, recipient_id, message):
        # you probably use http to send a message
        # TODO http output channel
        """
        url = self.url
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

        # console output for testing purposes
        utils.print_color(message, self.default_output_color)
        print(message)

        data = {"sender": "testsender",
                "message": message}
        print(recipient_id)
        headers = {"Content-type": "application/json"}
        requests.post(recipient_id,
                      headers=headers,
                      data=json.dumps(data))


class VoiceInput(HttpInputComponent):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    def __init__(self, url, access_token=None):
        self.out_channel = VoiceOutput(url, access_token)

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/message", methods=['POST'])
        def message():
            payload = request.json
            sender_id = payload.get("sender", None)
            text = payload.get("message", None)

            on_new_message(UserMessage(text, self.out_channel, sender_id))

            return "success"

        return custom_webhook