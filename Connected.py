import socket
import sys
import time
import traceback

from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget

from Client import ChatClient
import hashlib

from GroupChat import GroupChat
from OneToOneChat import OneToOneChat


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

        # self.selected_client_index = self.qlist_connected_clients.selectionChanged()

        vbox_connected_clients.addWidget(self.qlist_connected_clients)

        self.clientThread = GetClientsThread(self.client)
        self.clientThread.all_clients_and_groups.connect(self.get_all_info_lists)

        self.clientThread.start()

        # Connected Clients Buttons
        chat_1_to_1_btn = QPushButton("1:1 Chat")
        chat_1_to_1_btn.clicked.connect(self.one_to_one_chat)

        # Top section
        hbox_top_section = QHBoxLayout()
        hbox_top_section.addLayout(vbox_connected_clients)
        hbox_top_section.addWidget(chat_1_to_1_btn)

        # Chat Rooms
        vbox_chat_rooms = QVBoxLayout()
        vbox_chat_rooms.addWidget(QLabel("Chat rooms (Group chat)"))
        self.qlist_chat_rooms = QListWidget()
        vbox_chat_rooms.addWidget(self.qlist_chat_rooms)

        # Chat room buttons
        vbox_room_buttons = QVBoxLayout()
        room_create_btn = QPushButton("Create")
        room_create_btn.clicked.connect(self.create_room)
        room_join_btn = QPushButton("Join")
        room_join_btn.clicked.connect(self.group_chat)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
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

    def get_all_info_lists(self, all_clients_and_groups):

        # print(all_clients_and_groups)

        all_client = all_clients_and_groups[0]
        all_group = all_clients_and_groups[1]

        if self.qlist_connected_clients.currentRow() != -1:
            self.selected_client_name = self.qlist_connected_clients.currentItem().text().split(" - ")[0]
        else:
            self.selected_client_name = ""

        if self.qlist_chat_rooms.currentRow() != -1:
            self.selected_chat_room_name = self.qlist_chat_rooms.currentItem().text().split(" - ")[0]
        else:
            self.selected_chat_room_name = ""

        if self.qlist_connected_clients.count() > len(all_client):
            self.qlist_connected_clients.reset()
            self.qlist_connected_clients.clear()

        if self.qlist_chat_rooms.count() > len(all_group):
            self.qlist_chat_rooms.reset()
            self.qlist_chat_rooms.clear()

        for client in all_client:
            is_found = False
            if client[0] == self.client_name:
                for i in range(self.qlist_connected_clients.count()):
                    try:

                        disp_cname = self.qlist_connected_clients.item(i).text().split(" - (me) ")[0]
                        disp_lapse_time = self.qlist_connected_clients.item(i).text().split(" - (me) ")[1]

                        if disp_cname == client[0]:
                            is_found = True
                            if disp_lapse_time != client[4]:
                                self.qlist_connected_clients.item(i).setText(client[0] + " - (me) " + client[4])
                    except IndexError:
                        pass
                if not is_found:
                    self.qlist_connected_clients.addItem(client[0] + " - (me) " + client[4])
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

        for room in all_group:
            is_found_room = False
            for i in range(self.qlist_chat_rooms.count()):
                try:
                    disp_rname = self.qlist_chat_rooms.item(i).text().split(" by ")[0]
                    disp_owner_name = self.qlist_chat_rooms.item(i).text().split(" by ")[1]
                    if disp_rname == room[0][0]:
                        is_found_room = True
                except IndexError:
                    pass
            if not is_found_room:
                self.qlist_chat_rooms.addItem(room[0][0] + " by " + room[0][1])

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def close(self):
        self.clientThread.stop()
        time.sleep(0.3)
        self.client.cleanup()
        self.hide()
        self.prev_gui.show()

    def create_room(self):
        self.client.create_new_room()

    def one_to_one_chat(self, client):

        if self.selected_client_name == "":
            # print("you have to select at least one")
            QMessageBox.warning(self, 'Error!', 'you have to select at least one user')
        elif self.selected_client_name == self.client_name:
            # print("you cannot chat to yourself")
            QMessageBox.warning(self, 'Error!', 'you cannot chat to yourself')
        else:
            self.clientThread.stop()
            time.sleep(0.3)
            self.one_to_one = OneToOneChat(self.client, self.client_name, self.selected_client_name, self, self.clientThread)
            self.hide()
            self.one_to_one.show()

    # Transition to Group Chat Rooms
    def group_chat(self, client):

        if self.selected_chat_room_name == "":
            # print("you have to select at least one")
            QMessageBox.warning(self, 'Error!', 'you have to select at least one group')
        else:
            self.clientThread.stop()
            time.sleep(0.3)
            self.group_chat_room = GroupChat(self.client, self.client_name, self.selected_chat_room_name.split(" ")[0], self, self.clientThread)
            self.hide()
            self.group_chat_room.show()


class GetClientsThread(QThread):
    all_clients_and_groups = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.Ready = True
        self.client = client

    def run(self):
        while self.Ready:
            data = self.client.get_client_and_group_list()
            time.sleep(0.2)
            if len(data) > 1:
                try:
                    # print(data)
                    self.all_clients_and_groups.emit(data)
                except TypeError as e:
                    pass

    def stop(self):
        self.Ready = False

    def restart(self):
        self.Ready = True
