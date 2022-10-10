import socket
import sys
import time

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget, QTextBrowser

from Client import ChatClient


class GroupChatInvite(QWidget):

    def __init__(self, client, group_id, room_message_thread, parse_member_thread):
        super().__init__()
        # self.prev_gui = prev_gui
        self.client = client
        self.group_id = group_id
        self.room_message_thread = room_message_thread
        self.parse_member_thread = parse_member_thread
        self.invite_client_name = ""
        self.initUI()

    def initUI(self):

        vbox_screen = QVBoxLayout()

        self.not_in_room_client = self.client.get_list_of_client_not_in_room(self.group_id)

        clients_label = QLabel(f"Connected Clients")
        clients_label.setFont(QFont('Times', 14))

        self.not_connected_clients_list = QListWidget()

        hbox_buttons = QHBoxLayout()

        invite_btn = QPushButton("Invite")
        invite_btn.setFont(QFont('Times', 14))
        invite_btn.clicked.connect(self.invite)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont('Times', 14))
        cancel_btn.clicked.connect(self.close)

        hbox_buttons.addWidget(invite_btn)
        hbox_buttons.addWidget(cancel_btn)

        # ENTIRE SCREEN
        vbox_screen.addWidget(clients_label)
        vbox_screen.addWidget(self.not_connected_clients_list)
        vbox_screen.addLayout(hbox_buttons)

        self.not_connected_clients_list.selectionModel().selectionChanged.connect(self.on_row_changed)

        self.setLayout(vbox_screen)

        self.setWindowTitle('')
        self.setGeometry(200, 200, 300, 600)

        for item in self.not_in_room_client:
            self.not_connected_clients_list.addItem(item)
#        self.show()

    def close(self):
        self.hide()

    def on_row_changed(self, current, previous):

        current_text = self.not_connected_clients_list.currentItem().text()
        self.invite_client_name = current_text

        # print(self.invite_client_name)

    def invite(self):

        if self.invite_client_name == "":
            QMessageBox.warning(self, 'Error!', 'You Have To Select At Least One Client To Invite!')
        else:
            self.client.invite_other_member(self.invite_client_name, self.group_id)
            self.hide()
            QMessageBox.warning(self, 'Invitation Sent',
                                f'You Have Just Sent the Invitation to {self.invite_client_name}!')


#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = GroupChatInvite("a", "b", "c")
#     sys.exit(app.exec_())

