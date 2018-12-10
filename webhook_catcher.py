from flask import Flask, request
app = Flask(__name__)


@app.route('/app/webhook', methods=['GET', 'POST'])
def app_webhook_route():
    print(request.data)

    return 'OK', 200


if __name__ == '__main__':
    app.run()
