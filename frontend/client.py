import requests
import json

from flask import Flask, request, render_template, session

app = Flask(__name__)


def user_input():
    # encoded_query = quote(query)
    message = input("User: ")
    url = "http://50f39933.ngrok.io/app/message"

    data = {"sender": "user", "message": message}
    data_json = json.dumps(data)
    headers = {'Content-Type': 'application/json'}

    r = requests.post(
        url=url,
        data=data_json,
        headers=headers
    )


@app.route("/", methods=['POST'])
def receive_bot_response():
    payload = request.json
    message = payload.get("message", None)
    print(f'Bot: {message}')
    user_input()

    return "success", 200


if __name__ == '__main__':
    #app.session_interface = SecureCookieSessionInterface()
    app.run()
    user_input()
