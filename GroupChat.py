import socket
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget, QTextBrowser

from Client import ChatClient


class GroupChat(QWidget):

    def __init__(self, client, group_id, prev_gui):
        super().__init__()
        self.prev_gui = prev_gui
        self.client = client
        self.group_id = group_id
        self.initUI()

    def initUI(self):

        vbox_left_screen = QVBoxLayout()

        # top part
        chat_with_label = QLabel(f"Room 1 by {'Alice'}")
        chat_with_label.setFont(QFont('Times', 14))

        message_browser = QTextBrowser()
        vbox_left_screen.addWidget(chat_with_label)
        vbox_left_screen.addWidget(message_browser)

        # sending message part
        hbox_send_message = QHBoxLayout()

        chat_message_box = QLineEdit()
        chat_message_box.setFont(QFont('Times', 14))

        send_text_btn = QPushButton("Send")
        send_text_btn.setFont(QFont('Times', 14))


        send_img_btn = QPushButton("Send Image")
        send_img_btn.setFont(QFont('Times', 14))

        hbox_send_message.addWidget(chat_message_box)
        hbox_send_message.addWidget(send_text_btn)
        hbox_send_message.addWidget(send_img_btn)

        vbox_left_screen.addLayout(hbox_send_message)

        # Close Button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont('Times', 14))
        vbox_left_screen.addWidget(close_btn)


        # RIGHT SCREEN
        vbox_right_screen = QVBoxLayout()

        members_label = QLabel(f"Members")
        members_label.setFont(QFont('Times', 14))

        members_list = QListWidget()

        invite_btn = QPushButton("Invite")
        invite_btn.setFont(QFont('Times', 14))

        vbox_right_screen.addWidget(members_label)
        vbox_right_screen.addWidget(members_list)
        vbox_right_screen.addWidget(invite_btn)

        # ENTIRE SCREEN
        hbox_entire_screen = QHBoxLayout()

        hbox_entire_screen.addLayout(vbox_left_screen)
        hbox_entire_screen.addLayout(vbox_right_screen)

        self.setLayout(hbox_entire_screen)

        self.setWindowTitle('')
        self.setGeometry(200, 200, 600, 600)
#         self.show()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = GroupChat("a", "b", "c")
#     sys.exit(app.exec_())

