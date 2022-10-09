import difflib
import os
import socket
import sys
import time
import uuid

from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox, QListWidget, QTextBrowser, QTextEdit, QListWidgetItem, QFileDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui

from Client import ChatClient
from PictureViewer import PictureViewer


class GroupChat(QWidget):

    def __init__(self, client, client_name, group_name, prev_gui, client_thread):
        super().__init__()
        self.prev_gui = prev_gui
        self.client = client
        self.client_name = client_name
        self.group_name = group_name
        self.client_thread = client_thread
        self.initUI()

    def initUI(self):

        self.register_in_room()

        vbox_entire_screen = QVBoxLayout()

        self.dlg = QFileDialog()

        self.file_size = 0
        self.original_file_b_data = b''

        self.selected_file_name = ""


        # top part
        chat_with_label = QLabel(f"{self.group_name}")
        chat_with_label.setFont(QFont('Times', 14))

        self.message_browser = QListWidget()
        vbox_entire_screen.addWidget(chat_with_label)
        vbox_entire_screen.addWidget(self.message_browser)

        self.message_browser.selectionModel().selectionChanged.connect(self.on_row_changed)
        self.message_browser.setIconSize(QtCore.QSize(200, 200))

        time.sleep(0.3)
        self.room_message_thread = RoomMessageThread(self.client)
        self.room_message_thread.member_messages.connect(self.update_room_members)
        self.room_message_thread.messages.connect(self.update_chat_message_record)
        self.room_message_thread.start()

        self.parse_member_thread = ParseMemberThread(self.client)
        self.parse_member_thread.start()

        # Picture Buttons
        view_pic_btn = QPushButton("View Selected Picture")
        view_pic_btn.clicked.connect(self.view_image)
        download_pic_button = QPushButton("Download Selected Picture")
        download_pic_button.clicked.connect(self.save_files)
        hbox_pic = QHBoxLayout()

        hbox_pic.addWidget(view_pic_btn)
        hbox_pic.addWidget(download_pic_button)

        # sending message part
        hbox_send_message = QHBoxLayout()

        self.chat_message_box = QLineEdit()
        self.chat_message_box.setFont(QFont('Times', 14))

        send_text_btn = QPushButton("Send")
        send_text_btn.setFont(QFont('Times', 14))
        send_text_btn.clicked.connect(self.send_message)


        send_img_btn = QPushButton("Send Image")
        send_img_btn.setFont(QFont('Times', 14))
        send_img_btn.clicked.connect(self.get_files)

        hbox_send_message.addWidget(self.chat_message_box)
        hbox_send_message.addWidget(send_text_btn)
        hbox_send_message.addWidget(send_img_btn)

        vbox_entire_screen.addLayout(hbox_pic)
        vbox_entire_screen.addLayout(hbox_send_message)

        # Close Button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont('Times', 14))
        close_btn.clicked.connect(self.close)
        vbox_entire_screen.addWidget(close_btn)

        # Right SCREEN
        vbox_right_screen = QVBoxLayout()

        members_label = QLabel(f"Members")
        members_label.setFont(QFont('Times', 14))

        self.members_list = QListWidget()

        invite_btn = QPushButton("Invite")
        invite_btn.setFont(QFont('Times', 14))

        vbox_right_screen.addWidget(members_label)
        vbox_right_screen.addWidget(self.members_list)
        vbox_right_screen.addWidget(invite_btn)

        hbox_entire_screen = QHBoxLayout()

        hbox_entire_screen.addLayout(vbox_entire_screen)
        hbox_entire_screen.addLayout(vbox_right_screen)

        self.setLayout(hbox_entire_screen)

        self.setWindowTitle('')
        self.setGeometry(200, 200, 600, 600)
        # self.show()


    def view_image(self):
        # print(f"--------{self.selected_file_name}---------")
        if self.selected_file_name != "":
            self.dialog = PictureViewer(self.selected_file_name)
            self.dialog.show()
    def on_row_changed(self, current, previous):

        current_text = self.message_browser.currentItem().text()

        if (".jpg" in current_text) or (".png" in current_text):
            self.selected_file_name = current_text
        else:
            self.selected_file_name = ""

        print(self.selected_file_name)

    def register_in_room(self):

        data = []
        data.append("group-register")
        data.append(self.group_name)
        data.append(self.client_name)

        # print(data)
        self.client.join_new_room(data)

    def deregister_from_room(self):

        data = []
        data.append("group-deregister")
        data.append(self.group_name)
        data.append(self.client_name)

        self.client.leave_room(data)

    def update_room_members(self, member_messages):


        if "127.0.0.1" in str(member_messages):
            print("WRONG!")
        else:
            print(member_messages)


    def update_chat_message_record(self, messages):

        # print(messages[0])

        if type(messages[0]) == str:

            self.message_browser.addItem(messages[0])

            # img = QListWidgetItem()
            # img.setIcon(QIcon("111.png"))
            # img.setSizeHint(QSize(100, 100))
            # self.message_browser.addItem(img)

        elif len(messages) == 4:
            self.file_size += len(messages[0])
            if self.file_size != messages[3]:
                self.original_file_b_data += messages[0]
            else:
                # message[2] file_name
                image_file = open(f"{messages[2]}", "wb")
                image_file.write(self.original_file_b_data)
                time.sleep(0.2)
                image_file.close()
                self.original_file_b_data = b''
                self.file_size = 0

                img = QListWidgetItem()
                # apply transparent color to texts
                img.setForeground(QColor(255, 255, 255, 0))
                img.setIcon(QIcon(f"{messages[2]}"))
                img.setText(f"{messages[2]}")
                img.setSizeHint(QSize(200, 200))

                self.message_browser.addItem(messages[1])
                self.message_browser.addItem(img)


    def save_files(self):

        if self.selected_file_name != "":

            name = QFileDialog.getSaveFileName(self, 'Save File')

            extension = self.selected_file_name.split(".")
            extension_name = "." + extension[len(extension) - 1]

            file_to_save = open(name[0] + extension_name, 'wb')

            file_open = open(f"{self.selected_file_name}", 'rb')
            with file_open:
                img_data = file_open.read()
            file_open.close()

            file_to_save.write(img_data)
            file_to_save.close()


    def get_files(self):
        self.dlg.setFileMode(QFileDialog.AnyFile)
        self.filenames = ""

        if self.dlg.exec_():
            self.filenames = self.dlg.selectedFiles()
            # print(self.filenames)
            f = open(self.filenames[0], 'rb')
            extension = self.filenames[0].split(".")
            extension_name = "." + extension[len(extension)-1]
            # print(f)

            with f:
                img_data = f.read()
                # print(data)

            sent_file_size = len(img_data)

            n = 5000
            img_data_list = [img_data[i:i + n] for i in range(0, len(img_data), n)]
            # print(len(img_data_list))
            # print(img_data_list[0])


            for data_element in img_data_list:

                data = []
                data.append("chat-img")
                filename = str(uuid.uuid4())
                data.append(filename + extension_name)
                data.append(self.client_name)
                data.append(self.other_client_name)
                data.append(data_element)
                data.append(sent_file_size)
                # print(data)
                self.client.send_message(data)



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




    def close(self):
        time.sleep(0.2)
        self.room_message_thread.stop()
        time.sleep(0.2)
        self.parse_member_thread.stop()
        time.sleep(0.2)

        self.hide()
        self.prev_gui.show()
        time.sleep(0.2)
        self.client_thread.restart()
        self.client_thread.start()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            event.accept()
        else:
            event.ignore()

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = GroupChat("s","dd","rrrr","ddd","rrrr")
#     sys.exit(app.exec_())

class ParseMemberThread(QThread):
    def __init__(self, client):
        super().__init__()
        self.ready = True
        self.client = client

    def run(self):
        while self.ready:
            time.sleep(0.2)
            self.client.receive_group_list_only()

    def stop(self):
        self.ready = False

    def restart(self):
        self.ready = True


class RoomMessageThread(QThread):

    messages = pyqtSignal(list)
    member_messages = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.ready = True
        self.client = client
        self.message_switch = False

    def run(self):
        while self.ready:
            try:
                data = self.client.receive_message()
                if type(data[0]) == str:
                    self.messages.emit(data)
                else:
                    self.member_messages.emit(data)
            except TypeError as e:
                pass

    def stop(self):
        self.ready = False

    def restart(self):
        self.ready = True
