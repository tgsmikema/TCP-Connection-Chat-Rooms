import socket
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget

from Client import ChatClient


class Connected(QWidget):

    def __init__(self, client, prev_gui):
        super().__init__()
        self.prev_gui = prev_gui
        self.client = client
        self.initUI()

    def initUI(self):

        # Connected Clients
        vbox_connected_clients = QVBoxLayout()
        vbox_connected_clients.addWidget(QLabel("Connected Clients"))
        qlist_connected_clients = QListWidget()
        vbox_connected_clients.addWidget(qlist_connected_clients)


        # Connected Clients Buttons
        chat_1_to_1_btn = QPushButton("1:1 Chat")


        # Top section
        hbox_top_section = QHBoxLayout()
        hbox_top_section.addLayout(vbox_connected_clients)
        hbox_top_section.addWidget(chat_1_to_1_btn)

        # Chat Rooms
        vbox_chat_rooms = QVBoxLayout()
        vbox_chat_rooms.addWidget(QLabel("Chat rooms (Group chat)"))
        qlist_chat_rooms = QListWidget()
        vbox_chat_rooms.addWidget(qlist_chat_rooms)

        # Chat room buttons
        vbox_room_buttons = QVBoxLayout()
        room_create_btn = QPushButton("Create")
        room_join_btn = QPushButton("Join")
        close_btn = QPushButton("Close")
        vbox_room_buttons.addStretch(1)
        vbox_room_buttons.addWidget(room_create_btn)
        vbox_room_buttons.addWidget(room_join_btn)
        vbox_room_buttons.addStretch(1)
        vbox_room_buttons.addWidget(close_btn)

        # Bottom section
        hbox_bottom_section = QHBoxLayout()
        hbox_bottom_section.addLayout(vbox_chat_rooms)
        hbox_bottom_section.addLayout(vbox_room_buttons)

        # Entire Screen
        vbox_entire_screen = QVBoxLayout()
        vbox_entire_screen.addLayout(hbox_top_section)
        vbox_entire_screen.addLayout(hbox_bottom_section)

        self.setLayout(vbox_entire_screen)

        self.setWindowTitle('')
        self.setGeometry(200, 200, 600, 600)


