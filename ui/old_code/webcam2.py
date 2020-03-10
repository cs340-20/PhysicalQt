from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import os
import sys

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.online_webcams = QCameraInfo.availableCameras()
        if not self.online_webcams:
            pass #quit
        self.exist = QCameraViewfinder()
        self.exist.show()
        self.setCentralWidget(self.exist)

        # size
        self.left = 5
        self.top = 5
        self.width = 580
        self.height = 480

        # add a buttom
        button = QPushButton('Test', self)
        button.clicked.connect(self.handleButton)
        layout = QHBoxLayout(self)
        layout.addWidget(button)

        # set the default webcam.
        self.get_webcam(0)
        self.setWindowTitle("WebCam")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def get_webcam(self, i):
        self.my_webcam = QCamera(self.online_webcams[i])
        self.my_webcam.setViewfinder(self.exist)
        self.my_webcam.setCaptureMode(QCamera.CaptureStillImage)
        self.my_webcam.error.connect(lambda: self.alert(self.my_webcam.errorString()))
        self.my_webcam.start()

    def alert(self, s):
        """
        This handle errors and displaying alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(s)

    def handleButton(self):
        print ('Hello World')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("WebCam")

    #button = QPushButton('PyQt5 button', self)
    #button.setToolTip('This is an example button')
    #button.move(100,70)

    window = MainWindow()
    app.exec_()
