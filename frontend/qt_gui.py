import requests
import json
import threading

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QTcpSocket

from http.server import BaseHTTPRequestHandler, HTTPServer


class ChatWindow(QDialog, BaseHTTPRequestHandler):
    def __init__(self, request, clien_):
        super().__init__()

        server_address = ('127.0.0.1', 8081)
        httpd = HTTPServer(server_address, self)
        thread = threading.Thread(target=httpd.serve_forever())
        thread.start()

        self.initWindow()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data.decode('utf-8').replace("'", '"'))
        self.chatWindow.append(json_data['message'])

        # response
        self._set_headers()
        message = "Hello POST!"
        self.wfile.write(bytes(message, "utf8"))


    def initWindow(self):
        self.label = QLabel('Listening')

        self.chatWindow = QTextEdit(self)
        self.chatWindow.setReadOnly(True)

        self.inputField = QLineEdit(self)

        self.startButton = QPushButton('Start', self)
        #self.startButton.move(50, 400)
        #self.startButton.setGeometry(40, 400, 50, 50)
        self.startButton.clicked.connect(self.startBot)

        self.sendButton = QPushButton('Senden', self)
        #self.startButton.setGeometry(60, 400, 50, 50)
        self.sendButton.clicked.connect(self.send_message)

        self.chatLayout = QVBoxLayout(self)
        self.chatLayout.addWidget(self.label)
        self.chatLayout.addWidget(self.chatWindow)
        self.chatLayout.addWidget(self.inputField)
        self.chatLayout.addWidget(self.startButton)
        self.chatLayout.addWidget(self.sendButton)

        self.setGeometry(500, 200, 500, 500)
        self.setWindowTitle('Carebot')

        self.show()

    def httpSendMessage(self, message):
        url = "http://bce96cee.ngrok.io/app/message"

        data = {"sender": "user", "message": "/start"}
        data_json = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        requests.post(
            url=url,
            data=data_json,
            headers=headers
        )

    def httpGetMessage(self):
        url = "http://bce96cee.ngrok.io/app/message"
        headers = {'Content-Type': 'application/json'}

        new_message = requests.get(
            url=url
        )

        return new_message

    def send_message(self, message):
        self.httpSendMessage(message)

    def startBot(self, message):
        self.httpSendMessage(message)
        self.chatWindow.append('Guten Tag')

    def display_new_message(self):
        new_message = self.httpGetMessage()
        if new_message:
            self.chatWindow.append(new_message)


if __name__ == '__main__':
    app = QApplication([])
    window = ChatWindow()

    timer = QTimer()
    timer.timeout.connect(window.display_new_message)
    timer.start(1000)

    app.exec_()
