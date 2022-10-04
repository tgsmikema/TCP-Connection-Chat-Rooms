import socket
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget, QTextBrowser

from Client import ChatClient


class GroupChatInvite(QWidget):

    def __init__(self, client, group_id, prev_gui):
        super().__init__()
        self.prev_gui = prev_gui
        self.client = client
        self.group_id = group_id
        self.initUI()

    def initUI(self):


        vbox_screen = QVBoxLayout()

        clients_label = QLabel(f"Connected Clients")
        clients_label.setFont(QFont('Times', 14))

        connected_clients_list = QListWidget()

        hbox_buttons = QHBoxLayout()

        invite_btn = QPushButton("Invite")
        invite_btn.setFont(QFont('Times', 14))

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont('Times', 14))

        hbox_buttons.addWidget(invite_btn)
        hbox_buttons.addWidget(cancel_btn)

        # ENTIRE SCREEN
        vbox_screen.addWidget(clients_label)
        vbox_screen.addWidget(connected_clients_list)
        vbox_screen.addLayout(hbox_buttons)


        self.setLayout(vbox_screen)

        self.setWindowTitle('')
        self.setGeometry(200, 200, 300, 600)
#         self.show()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = GroupChatInvite("a", "b", "c")
#     sys.exit(app.exec_())

