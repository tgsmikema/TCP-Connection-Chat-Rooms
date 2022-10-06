import socket
import sys
import time
import traceback

from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget

from Client import ChatClient
import hashlib


class Connected(QWidget):

    def __init__(self, client, prev_gui):
        super().__init__()
        self.prev_gui = prev_gui
        self.client = client
        self.initUI()

    def initUI(self):

        self.client_name = self.client.get_own_name()

        # Connected Clients
        vbox_connected_clients = QVBoxLayout()
        vbox_connected_clients.addWidget(QLabel("Connected Clients"))
        self.qlist_connected_clients = QListWidget()
        vbox_connected_clients.addWidget(self.qlist_connected_clients)

        self.clientThread = GetClientsThread(self.client)
        self.clientThread.allClients.connect(self.get_all_info_lists)

        self.clientThread.start()

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

    def get_all_info_lists(self, allClients):

        if self.qlist_connected_clients.count() > len(allClients):
            self.qlist_connected_clients.reset()
            self.qlist_connected_clients.clear()

        for client in allClients:
            is_found = False
            if client[0] == self.client_name:
                for i in range(self.qlist_connected_clients.count()):
                    try:

                        disp_cname = self.qlist_connected_clients.item(i).text().split(" (me) ")[0]
                        disp_lapse_time = self.qlist_connected_clients.item(i).text().split(" (me) ")[1]

                        if disp_cname == client[0]:
                            is_found = True
                            if disp_lapse_time != client[4]:
                                self.qlist_connected_clients.item(i).setText(client[0] + " (me) " + client[4])
                    except IndexError:
                        pass
                if not is_found:
                    self.qlist_connected_clients.addItem(client[0] + " (me) " + client[4])
            else:
                for i in range(self.qlist_connected_clients.count()):
                    try:

                        disp_cname = self.qlist_connected_clients.item(i).text().split(" - ")[0]

                        disp_lapse_time = self.qlist_connected_clients.item(i).text().split(" - ")[1]

                        if disp_cname == client[0]:
                            is_found = True
                            if disp_lapse_time != client[4]:
                                self.qlist_connected_clients.item(i).setText(client[0] + " - " + client[4])
                    except IndexError:
                        pass
                if not is_found:
                    self.qlist_connected_clients.addItem(client[0] + " - " + client[4])



class GetClientsThread(QThread):
    allClients = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.Ready = True
        self.client = client

    def run(self):
        while self.Ready:
            data = self.client.get_client_and_group_list()
            time.sleep(0.2)
            try:
                # print(data)
                self.allClients.emit(data)
            except TypeError as e:
                pass

    def stop(self):
        self.Ready = False

    def restart(self):
        self.Ready = True
