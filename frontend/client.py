import requests
import json


def send_api_request():
    """
    Sends a HTTP GET request to a published LUIS.ai app with message as URL param
    :param query: message to be handled
    :return: JSON response from LUIS.ai
    """
    # encoded_query = quote(query)

    data = {"sender": "http://127.0.0.1:5000",
            "message": "Hallo"}
    headers = {"Content-type": "application/json"}

    response = requests.post("https://b77597fa.ngrok.io/app/message",
                             headers=headers,
                             data=json.dumps(data))
    print(response.content)

    return response.content

