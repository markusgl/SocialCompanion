""" NLU using Microsoft LUIS.ai and maps it for Rasa dialogue management"""

from rasa_core.interpreter import RasaNLUInterpreter
import requests
import json
from rasa_nlu_schema import RasaNLUSchema, NLUResponse, EntitiesSchema, IntentSchema


class Interpreter(RasaNLUInterpreter):

    def __init__(self):
        keys_file = 'keys.json'
        with open(keys_file) as f:
            data = json.load(f)
        self.subscription_key = data['luis-subscription-key']

    def send_api_request(self, query):
        """
        Sends a HTTP GET request to a published LUIS.ai app with message as URL param
        :param query: message to be handled
        :return: JSON response from LUIS.ai
        """

        params = {"subscription-key": self.subscription_key,
                  "verbose": "true",
                  "timezoneOffset": 0,
                  "q": query
                  }

        response = requests.get(
            "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/f8f75a16-ba32-41e6-a10c-6f7b3aaf31f9",
            params=params)

        #print("LUIS response: %s" % response.content)

        return response.content


    def parse(self, message):
        """
        Converts the response from LUIS.ai to Rasa-NLU format
        :param message: message from user
        :return: dict following Rasa-NLU format
        """
        resp = json.loads((self.send_api_request(message)).decode('utf-8'))

        nlu_response = NLUResponse()
        nlu_response.text = message

        intent_schema = IntentSchema()

        intent_schema.name = resp["topScoringIntent"]["intent"]
        intent_schema.confidence = resp["topScoringIntent"]["score"]
        nlu_response.intent = intent_schema

        try:
            entities = resp["entities"]

            nlu_response.entities = []
            for entity in entities:
                entity_schema = EntitiesSchema()
                entity_schema.start = entity["startIndex"]
                entity_schema.end = entity["endIndex"]
                entity_schema.value = entity["entity"]
                entity_schema.entity = entity["type"]
                nlu_response.entities.append(entity_schema)

        except Exception as err:
            print(err)
            print("Decoding failed")

        schema = RasaNLUSchema()
        data, error = schema.dump(nlu_response)

        return data
