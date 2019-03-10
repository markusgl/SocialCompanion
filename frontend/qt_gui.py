import requests
import json

from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initWindow()

    def initWindow(self):
        self.startButton = QPushButton('Start', self)
        self.startButton.move(50, 400)
        self.startButton.clicked.connect(self.startBot)

        self.chatLayout = QVBoxLayout(self)
        self.chatWindow = QTextEdit(self)
        self.chatWindow.setReadOnly(True)
        self.label = QLabel('Listening')

        self.chatLayout.addWidget(self.label)
        self.chatLayout.addWidget(self.chatWindow)
        self.chatLayout.addWidget(self.startButton)

        self.setGeometry(500, 200, 500, 500)
        self.setWindowTitle('Carebot')

        self.show()

    def startBot(self):
        url = "http://5e8e6b19.ngrok.io/app/message"

        data = {"sender": "user", "message": "/start"}
        data_json = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        requests.post(
            url=url,
            data=data_json,
            headers=headers
        )

        self.chatWindow.append('Guten Tag')

    def appendMessage(self, message):
        self.chatWindow.append(message)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()

