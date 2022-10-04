import socket
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget

from Client import ChatClient


class OneToOneChat(QWidget):

    def __init__(self, client, other_client, prev_gui):
        super().__init__()
        self.prev_gui = prev_gui
        self.client = client
        self.other_client = other_client
        self.initUI()

    def initUI(self):
        chat_with_label = QLabel(f"Chat with {'Alice'}")
        