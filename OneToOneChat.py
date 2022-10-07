import socket
import sys
import time

from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget, QTextBrowser

from Client import ChatClient


class OneToOneChat(QWidget):

    def __init__(self, client, client_name, other_client_name, prev_gui, client_thread):
        super().__init__()
        self.prev_gui = prev_gui
        self.client = client
        self.client_name = client_name
        self.other_client_name = other_client_name
        self.client_thread = client_thread
        self.initUI()

    def initUI(self):

        vbox_entire_screen = QVBoxLayout()

        # top part
        chat_with_label = QLabel(f"Chat with {self.other_client_name}")
        chat_with_label.setFont(QFont('Times', 14))

        self.message_browser = QTextBrowser()
        vbox_entire_screen.addWidget(chat_with_label)
        vbox_entire_screen.addWidget(self.message_browser)


        self.receive_msg_thread = ReceiveMessageThread(self.client)
        self.receive_msg_thread.messages.connect(self.update_chat_message_record)

        self.receive_msg_thread.start()

        # sending message part
        hbox_send_message = QHBoxLayout()

        self.chat_message_box = QLineEdit()
        self.chat_message_box.setFont(QFont('Times', 14))

        send_text_btn = QPushButton("Send")
        send_text_btn.setFont(QFont('Times', 14))
        send_text_btn.clicked.connect(self.send_message)


        send_img_btn = QPushButton("Send Image")
        send_img_btn.setFont(QFont('Times', 14))

        hbox_send_message.addWidget(self.chat_message_box)
        hbox_send_message.addWidget(send_text_btn)
        hbox_send_message.addWidget(send_img_btn)

        vbox_entire_screen.addLayout(hbox_send_message)

        # Close Button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont('Times', 14))
        vbox_entire_screen.addWidget(close_btn)

        self.setLayout(vbox_entire_screen)

        self.setWindowTitle('')
        self.setGeometry(200, 200, 600, 600)
        # self.show()

    def update_chat_message_record(self, messages):
        # doc = self.message_browser.toPlainText()
        # txt = str(doc).split('\n')
        # print(txt)
        if type(messages[0]) == str:
            self.message_browser.append(messages[0])

    def send_message(self):
        msg = self.chat_message_box.text()
        if len(msg) == 0:
            QMessageBox.warning(self, 'Error!', 'You Cannot Send An Empty Message!')
        else:
            data = []
            data.append("chat")
            data.append(self.client_name)
            data.append(self.other_client_name)
            data.append(msg)
            self.client.send_message(data)
            self.chat_message_box.clear()

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = OneToOneChat(client="s",other_client="d",prev_gui="f")
#     sys.exit(app.exec_())


class ReceiveMessageThread(QThread):
    messages = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.ready = True
        self.client = client

    def run(self):
        while self.ready:
            data = self.client.receive_message()
            time.sleep(0.2)
            if len(data) == 1:
                try:
                    self.messages.emit(data)
                except TypeError as e:
                    pass

    def stop(self):
        self.ready = False

    def restart(self):
        self.ready = True