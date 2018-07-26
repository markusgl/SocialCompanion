from flask import Flask, request, render_template, session

app = Flask(__name__)

@app.route("/respond", methods=['POST'])
def receive_bot_response():
    payload = request.json
    message = payload.get("message", None)
    print(message)


if __name__ == '__main__':
    #app.session_interface = SecureCookieSessionInterface()
    app.run()