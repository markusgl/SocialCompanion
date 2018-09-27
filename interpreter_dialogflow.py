""" NLU using Dialogflow (formerly API.ai) and maps it for Rasa dialogue management"""

from rasa_core.interpreter import RasaNLUInterpreter
import requests
import json
from rasa_nlu_schema import RasaNLUSchema, NLUResponse, EntitiesSchema, IntentSchema


class Interpreter(RasaNLUInterpreter):
    def __init__(self):
        #super(Interpreter, self)__init__()
        keys_file = 'keys.json'
        with open(keys_file) as f:
            data = json.load(f)
        self.session_id = data['dialogflow-session-id']
        self.bearer_token = data['dialogflow-bearer-token']

    def check_connection(self):
        query = 'hall%20hola'
        params = {"v": "20170712",
                  "query": query,
                  "lang": "de",
                  "sessionId": self.session_id,
                  "timezone": "Europe/Berlin"
                  }
        headers = {"Authorization": self.bearer_token}

        try:
            response = requests.get(
                "https://api.dialogflow.com/v1/query",
                params=params, headers=headers)
        except:
            return False

        if response.status_code == 200:
            return True
        else:
            return False

    def send_api_request(self, query):
        """
        Sends a HTTP GET request to a published LUIS.ai app with message as URL param
        :param query: message to be handled
        :return: JSON response from LUIS.ai
        """

        params = {"v": "20170712",
                  "query": query,
                  "lang": "de",
                  "sessionId": self.session_id,
                  "timezone": "Europe/Berlin"
                  }
        headers = {"Authorization": self.bearer_token}

        response = requests.get(
            "https://api.dialogflow.com/v1/query",
            params=params, headers=headers)

        #for debugging
        #print(response.url)
        print("Dialogflow response: %s" % response.content)

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
        if resp["result"]["metadata"]:
            intent_schema.name = resp["result"]["metadata"]["intentName"]
            intent_schema.confidence = resp["result"]["score"]
        else: # fallback if no intent is given by the nlu
            intent_schema.name = "greet"
            intent_schema.confidence = 0.0
        nlu_response.intent = intent_schema
        print("Recognized Intent by Dialogflow {}".format(intent_schema.name ))

        try:
            entities = resp["result"]["parameters"]
            resolved_query = resp["result"]["resolvedQuery"]

            nlu_response.entities = []
            for key, value in entities.items():
                if value:
                    entity_schema = EntitiesSchema()
                    entity_schema.start = resolved_query.find(value)
                    entity_schema.end = resolved_query.find(value) + len(value)
                    entity_schema.entity = key
                    entity_schema.value = value
                    nlu_response.entities.append(entity_schema)
                    #print("Key: {}, Value: {}".format(key, value))
        except Exception as err:
            print(err)
            print('No Entites extracted')

        schema = RasaNLUSchema()
        data, error = schema.dump(nlu_response)

        return data


if __name__ == '__main__':
    print(Interpreter().check_connection())
