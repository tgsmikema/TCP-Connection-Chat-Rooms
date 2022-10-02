import socket
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QLineEdit, QMessageBox

from Client import ChatClient


class Connection(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('IP address'), 0, 0)
        grid.addWidget(QLabel('Port'), 1, 0)
        grid.addWidget(QLabel('Nick Name'), 2, 0)

        self.ip_address = QLineEdit()
        self.ip_address.setText("127.0.0.1")
        self.port = QLineEdit()
        self.nick_name = QLineEdit()

        grid.addWidget(self.ip_address, 0, 1)
        grid.addWidget(self.port, 1, 1)
        grid.addWidget(self.nick_name, 2, 1)

        self.connect_btn = QPushButton("Connect")
        self.cancel_btn = QPushButton("Cancel")

        grid.addWidget(self.connect_btn, 3, 2)
        self.connect_btn.clicked.connect(self.connecting)

        grid.addWidget(self.cancel_btn, 3, 3)
        self.cancel_btn.clicked.connect(self.close)

        self.setWindowTitle('Chat Connection')
        self.setGeometry(300, 300, 800, 500)
        self.show()



    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def connecting(self):
        ip_address = self.ip_address.text()
        port = int(self.port.text())
        nick_name = self.nick_name.text()

        client = ChatClient(host=ip_address, port=port, name=nick_name)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Connection()
    sys.exit(app.exec_())
