import requests
import json
import threading
import sys
import socket

from threading import Thread
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QTcpSocket

from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

HOST, PORT = '127.0.0.1', 5000

#TODO - chat gui with http endpoint

class ChatWindow(QDialog):
    message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        #self.initWindow()

#    def initWindow(self):
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
        #self.show()

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

    def send_message(self, message):
        self.httpSendMessage(message)

    def startBot(self, message):
        self.httpSendMessage(message)
        self.chatWindow.append('Guten Tag')

    def display_new_message(self, message):
        self.chatWindow.append(message)


class HttpDaemon(QThread):
    def __init__(self):
        super().__init__()
        #self.window = ChatWindow()

    def run(self):
        app = QApplication(sys.argv)
        window = ChatWindow()
        window.show()
        app.exec_()
        QThread.terminate()

    def append(self, message):
        self.window.display_new_message(message)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        print('GET message received')
        self.window.display_new_message('Test')
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


if __name__ == '__main__':
    window = ChatWindow()

