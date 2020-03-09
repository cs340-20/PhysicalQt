# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhysicalQt.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
import numpy as np
import cv2

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

#class Ui_MainWindow(object):
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.webcam_capture = QtWidgets.QLabel(self.centralwidget)
        self.webcam_capture.setGeometry(QtCore.QRect(40, 60, 421, 311))
        self.webcam_capture.setScaledContents(True)
        self.webcam_capture.setObjectName("webcam_capture")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(40, 430, 141, 51))
        self.start.setObjectName("start")
        self.end = QtWidgets.QPushButton(self.centralwidget)
        self.end.setGeometry(QtCore.QRect(210, 430, 141, 51))
        self.end.setObjectName("end")
        self.motion = QtWidgets.QLabel(self.centralwidget)
        self.motion.setGeometry(QtCore.QRect(550, 60, 161, 331))
        self.motion.setScaledContents(True)
        self.motion.setObjectName("motion")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.start.clicked.connect(self.start_web_cam)
        self.end.clicked.connect(self.end_web_cam)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.webcam_capture.setText(_translate("MainWindow", "webcam"))
        self.start.setText(_translate("MainWindow", "start"))
        self.end.setText(_translate("MainWindow", "end"))
        self.motion.setText(_translate("MainWindow", "Exercise"))

    def start_web_cam(self):
        self.cap = cv2.VideoCapture(0)
        #while(True):
        ret, frame = self.cap.read()
        cv2.imwrite('webcam.png', frame)
        self.cap.release()

        self.webcam_capture.setPixmap(QtGui.QPixmap("webcam.png"))
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

    def end_web_cam(self):
        '''
        try:
            self.cap.release()
        except:
            pass
        '''
        self.webcam_capture.setPixmap(QtGui.QPixmap(''))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
