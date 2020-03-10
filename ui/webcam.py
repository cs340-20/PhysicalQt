import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

'''
class MainWindow(QWidget):
    def __init__(self, camera_index=0, fps=30):
        super().__init__()

        self.capture = cv2.VideoCapture(camera_index)
        self.dimensions = self.capture.read()[1].shape[1::-1]

        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)

        view = QGraphicsView(self)
        view.setScene(scene)

        text = QLabel('MegaWebcam 5.5', self)

        layout = QVBoxLayout(self)
        layout.addWidget(view)
        layout.addWidget(text)

        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()

    def get_frame(self):
        _, frame = self.capture.read()
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)

'''

class MainWindow(QWidget):
    def __init__(self, camera_index=0, fps=30):
        super().__init__()
        self.setFixedSize(850, 500)
        #self.setFixedSize(1050, 800)
        self.setWindowTitle('PhysicalQt')

        self.capture = cv2.VideoCapture(camera_index)

        self.image = QLabel(self)
        self.image.setGeometry(QRect(35, 35, 450, 300))
        # set location
        self.image2 = QLabel(self)
        self.image2.setGeometry(QRect(550, 35, 250, 300))

        text = QLabel('webcam', self)
        text.setGeometry(QRect(35, 5, 50, 25))
        text = QLabel('motion', self)
        text.setGeometry(QRect(550, 5, 50, 25))
        #layout = QVBoxLayout(self)
        '''
        layout = QHBoxLayout(self)
        layout.addWidget(self.image)
        #test
        layout.addWidget(self.image2)
        layout.addWidget(text)
        '''
        #text = QLabel('button', self)
        #text.setGeometry(QRect(35, 350, 36, 355))
        self.startb = QPushButton("start", self)
        self.startb.setGeometry(QRect(50, 350, 150, 60))
        self.end = QPushButton("end", self)
        self.end.setGeometry(QRect(200, 350, 150, 60))

        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()

    def get_frame(self):
        _, frame = self.capture.read()
        image = QImage(frame, *frame.shape[1::-1], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)
        self.image2.setPixmap(QPixmap("motion_sample.png"))
        self.image2.setScaledContents(True)

app = QApplication([])
win = MainWindow()
win.show()
app.exec()
