""" NLU using wit.ai and maps it for Rasa dialogue management"""

from rasa_core.interpreter import RasaNLUInterpreter
import requests
import json
import re
from rasa_nlu_schema import RasaNLUSchema, NLUResponse, EntitiesSchema, IntentSchema

class Interpreter(RasaNLUInterpreter):

    def __init__(self, keys_file='keys.json'):
        with open(keys_file) as f:
            data = json.load(f)
        self.bearer_token = data['witai-bearer-token']

    def send_api_request(self, query):
        """
        Sends a HTTP GET request to a published LUIS.ai app with message as URL param
        :param query: message to be handled
        :return: JSON response from LUIS.ai
        """

        params = {"v": "20180625",
                  "q": query
                  }
        headers = {"Authorization": self.bearer_token}

        response = requests.get(
            "https://api.wit.ai/message",
            params=params, headers=headers)

        #print("wit.ai response: %s" % response.content)

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
        if 'intent' in resp["entities"]:
            intent_schema.name = resp["entities"]["intent"][0]["value"]
            intent_schema.confidence = resp["entities"]["intent"][0]["confidence"]
        else:
            intent_schema.name = ''
            intent_schema.confidence = ''

        nlu_response.intent = intent_schema
        try:
            entities = resp["entities"]
            query = resp["_text"]
            #print(resp)
            nlu_response.entities = []
            for key, value in entities.items():
                if not key == 'intent':
                    entity_schema = EntitiesSchema()
                    entity_value = value[0]['value']

                    try:
                        a = re.search(entity_value, query.lower())
                        entity_schema.start = a.start()
                        entity_schema.end = a.start() + len(entity_value)
                    except:
                        print('Entity position not found')
                    entity_schema.entity = key
                    entity_schema.value = entity_value
                    nlu_response.entities.append(entity_schema)
                    print("Key: {}, Value: {}".format(key, value))
        except Exception as err:
            print(err)
            print("Decoding failed")


        schema = RasaNLUSchema()
        data, error = schema.dump(nlu_response)

        return data


interpreter = Interpreter()
data = interpreter.parse("Ich würde gerne ins Kino gehen")
print(data)
