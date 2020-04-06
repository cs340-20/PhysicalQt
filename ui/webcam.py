import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import os

sys.path.append('../posenet/core/')
import gt_interpreter as gt
import infer
from utils import packageCoordinateSetNormalized, gen_bounding_box, get_bbx_size

def get_qimage(image):
    height, width, channels = image.shape
    bytesPerLine = 3 * width
    image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
    image = image.rgbSwapped()
    return image


class DetectionWidget(QWidget, QRunnable):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pose_output = QImage()
        self.current_pose = None
        self.lastGoodFrame = 0

    def detect_pose(self, img):
        _, scores, coord = infer.infer(img)
        _out = packageCoordinateSetNormalized(scores, coord, (img.shape))
        self.current_pose = _out
        return _out

    @pyqtSlot()
    def gen_data(self, new_img_w, new_img_h, img, gt_item=None):
        # replace late if detect_pose isn't needed:
        pose_pack = self.detect_pose(img)
        img_blank = np.full((new_img_w,new_img_h, 3), 239, dtype=np.uint8)

        # generate bounding box size to figure out centering:
        #get_bbx_size(gen_bounding_box(pose_pack, ratio_w=new_img_w, ratio_h=new_img_h))
        #coord = gen_bounding_box(pose_pack, ratio_w=new_img_w, ratio_h=new_img_h)

        # draw gt:
        if gt_item != None:
            inst_item = gt_item[self.lastGoodFrame]
            for joint in inst_item.items():
                #true_size =
                true_size = (int(joint[1][2][1]*(new_img_w/1.5)), int(joint[1][2][0]*(new_img_h/2) + (new_img_h/3)))
                cv2.circle(img_blank, true_size, 5, (0,0,255), -1)

        # draw on blank canvas:
        for joint in pose_pack.items():
            true_size = (int(joint[1][2][1]*(new_img_w)), int(joint[1][2][0]*(new_img_h/2)+(new_img_h/3)))
            cv2.circle(img_blank, true_size, 3, (0,0,0), -1)
        self.pose_output = get_qimage(img_blank)
        if self.pose_output.size() != self.size():
            self.setFixedSize(self.pose_output.size())
        self.update()

class MainWindow(QWidget):
    def __init__(self, camera_index=0, fps=24):
        super().__init__()
        #self.threadpool = QThreadPool()
        self.mainStatus = False
        self.setFixedSize(900, 500)
        #self.setFixedSize(1050, 800)
        self.setWindowTitle('PhysicalQt')
        self.capture = cv2.VideoCapture(camera_index)

        # template load in:
        static_path = os.path.join(os.getcwd(), 'static')
        self.template_needstart = cv2.imread(os.path.join(static_path, 'template_needstart.png'))

        self.image = QLabel(self)
        self.image.setGeometry(QRect(35, 35, 450, 300))

        # set location
        self.image2 = QLabel(self)
        self.image2.setGeometry(QRect(550, 35, 300, 300))

        self.detectWidget = DetectionWidget()
        #self.threadpool.start(self.detectWidget)
        # load gt file manually here:
        self.gt_master, self.meta = gt.read_in_gt('../posenet/gt/jumping_jack/jumping_jack_02.json')

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
        self.startb = QPushButton("Start Tracking", self)
        self.startb.setGeometry(QRect(50, 350, 150, 60))
        self.startb.clicked.connect(lambda: self.switch_status())

        self.end = QPushButton("Stop Tracking", self)
        self.end.setGeometry(QRect(200, 350, 150, 60))
        self.end.clicked.connect(lambda: self.switch_status())

        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()

    def switch_status(self):
        self.mainStatus = not self.mainStatus

    def get_frame(self):
        _, frame = self.capture.read()

        if self.mainStatus:
            self.detectWidget.lastGoodFrame = (self.detectWidget.lastGoodFrame + 1) % self.meta[0]['meta']['total_frames']
            self.detectWidget.gen_data(300,300,frame, gt_item=self.gt_master[0])

            # Continously check pose:
            for i in range(len(self.gt_master[0])):
                gt.evaluate(self.detectWidget.current_pose, self.gt_master[0][i])

        image = QImage(frame, *frame.shape[1::-1], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

        if self.mainStatus:
            self.image2.setPixmap(QPixmap.fromImage(self.detectWidget.pose_output))
        else:
            self.image2.setPixmap(QPixmap.fromImage(get_qimage(self.template_needstart)))

        self.image2.setScaledContents(True)

app = QApplication([])
win = MainWindow()
win.show()
app.exec()
