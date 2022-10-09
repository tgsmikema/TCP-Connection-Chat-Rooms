import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PictureViewer(QWidget):

    def __init__(self, image_name):
        QWidget.__init__(self)
        self.image_name = image_name
        self.setup_ui()

    def setup_ui(self):
        self.image_label = QLabel()
        self.image_label.setMinimumSize(1500, 1000)
        self.pic_size = self.image_label.size()
        self.image_label.setPixmap(QPixmap(f'{self.image_name}').scaled(self.pic_size, Qt.KeepAspectRatio))

        self.main_layout = QVBoxLayout()  # adding widgets to layot
        self.main_layout.addWidget(self.image_label)

        self.setLayout(self.main_layout)  # set layot

        self.setWindowTitle('')
        self.setGeometry(200, 200, 600, 600)
        self.setMaximumSize(1200, 800)
        # self.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = PictureViewer("")
#     sys.exit(app.exec_())
