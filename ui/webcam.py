import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np

sys.path.append('../posenet/core/')
import gt_interpreter as gt
import infer
from utils import packageCoordinateSetNormalized

class DetectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pose_output = QImage()

    def detect_pose(self, img):
        _, scores, coord = infer.infer(img)
        _out = packageCoordinateSetNormalized(scores, coord, (img.shape))
        return _out

    def gen_data(self, new_img_w, new_img_h, img):
        # replace late if detect_pose isn't needed:
        # _, scores, coord = infer(img)
        pose_pack = self.detect_pose(img)
        #print(pose_pack)
        img_blank = np.full((new_img_w,new_img_h, 3), 125, dtype=np.uint8)
        # draw on blank canvas:
        for joint in pose_pack.items():
            true_size = (int(joint[1][2][1]*(new_img_w/2)), int(joint[1][2][0]*(new_img_h/2))+int(new_img_h/2))
            cv2.circle(img_blank, true_size, 3, (255,255,255))
        
        #cv2.circle(base_image, true_size, int(side*tolerance), (0,255,0), 1)
        self.pose_output = self.get_qimage(img_blank)
        if self.pose_output.size() != self.size():
            self.setFixedSize(self.pose_output.size())
        self.update()

    def get_qimage(self, image):
        height, width, channels = image.shape
        bytesPerLine = 3 * width
        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = image.rgbSwapped()
        return image

class MainWindow(QWidget):
    def __init__(self, camera_index=0, fps=30):
        super().__init__()
        self.setFixedSize(900, 500)
        #self.setFixedSize(1050, 800)
        self.setWindowTitle('PhysicalQt')

        self.capture = cv2.VideoCapture(camera_index)

        self.image = QLabel(self)
        self.image.setGeometry(QRect(35, 35, 450, 300))
        # set location
        self.image2 = QLabel(self)
        self.image2.setGeometry(QRect(550, 35, 300, 300))

        self.detectWidget = DetectionWidget() 

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
        
        #self.detectWidget.gen_data(frame.shape[0], frame.shape[0], frame)
        self.detectWidget.gen_data(300,300,frame)
        image = QImage(frame, *frame.shape[1::-1], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)
        
        self.image2.setPixmap(QPixmap.fromImage(self.detectWidget.pose_output))
        self.image2.setScaledContents(True)

app = QApplication([])
win = MainWindow()
win.show()
app.exec()
