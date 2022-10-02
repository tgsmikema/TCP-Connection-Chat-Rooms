import socket
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QLineEdit


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
        self.port = QLineEdit()
        self.nick_name = QLineEdit()

        grid.addWidget(self.ip_address, 0, 1)
        grid.addWidget(self.port, 1, 1)
        grid.addWidget(self.nick_name, 2, 1)

        connect_btn = QPushButton()
        cancel_btn = QPushButton()





        self.setWindowTitle('Box Layout')
        self.setGeometry(300, 300, 300, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Connection()
    sys.exit(app.exec_())