import requests
import json

def send_api_request():
    """
    Sends a HTTP GET request to a published LUIS.ai app with message as URL param
    :param query: message to be handled
    :return: JSON response from LUIS.ai
    """
    # encoded_query = quote(query)

    data = {"sender": "testsender",
            "message": "Ich heiße Markus"}

    headers = {"Content-type": "application/json"}

    response = requests.post("https://c89804d8.ngrok.io/app/message", headers=headers, data=json.dumps(data))
    print(response.content)

    return response.content

send_api_request()