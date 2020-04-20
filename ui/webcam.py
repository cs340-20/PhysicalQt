import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import os

import threading

sys.path.append('../posenet/core/')
import gt_interpreter as gt
import infer
from utils import packageCoordinateSetNormalized, gen_bounding_box, get_bbx_size, scale_pose, bind_pose_loc, normalization_fix

def get_qimage(image):
    height, width, channels = image.shape
    bytesPerLine = 3 * width
    image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
    image = image.rgbSwapped()
    return image


class DetectionWidget(QWidget, QRunnable):
    def __init__(self, parent=None, gt=None):
        # don't store images in class objects
        super().__init__(parent)
        self.gt = gt
        self.current_pose = None # coordinates
        self.lastGoodFrame = 0

    def detect_pose(self, img):
        _, scores, coord = infer.infer(img)
        _out = packageCoordinateSetNormalized(scores, coord, (img.shape))
        self.current_pose = _out
        return _out

    def draw_gt(self, gt_img):
        # try doing this multithreaded to make the gt not laggy with the model:
        # draw gt:
        width, height, _ = gt_img.shape
        if self.gt != None:
            inst_item = self.gt[self.lastGoodFrame]
            for joint in inst_item.items():
                true_size = normalization_fix(joint[1][2], width, height)
                #true_size = (int(joint[1][2][1]*(width/1.5)), int(joint[1][2][0]*(height/2) + (height/3)))
                cv2.circle(gt_img, true_size, 5, (0,0,255), -1)


    @pyqtSlot()
    def gen_output_pose(self, input_img, output_img):
        width, height, _ = output_img.shape

        # replace late if detect_pose isn't needed:
        pose_pack = self.detect_pose(input_img)

        # generate bounding box size to figure out centering:
        # use self.gt to access the ground truths:

        gt = self.gt[self.lastGoodFrame]
        posenet_bbox = gen_bounding_box(pose_pack, ratio_w=width, ratio_h=height)
        gt_bbox = gen_bounding_box(gt, ratio_w=width, ratio_h=height)

        coord1, coord2 = posenet_bbox[0], posenet_bbox[1]

        scale_out = scale_pose(gt_bbox, posenet_bbox, gt, pose_pack)
        new_pose = bind_pose_loc(gt, scale_out)
        #new_pose = bind_pose_loc(gt, pose_pack)

        # draw on blank canvas:
        for joint in new_pose.items():
            #true_size = (int(joint[1][2][1]*(width)), int(joint[1][2][0]*(height/2)+(height/3)))
            true_size = normalization_fix(joint[1][2], width, height)
            cv2.circle(output_img, true_size, 3, (0,0,0), -1)

        self.pose_output = get_qimage(output_img)
        if self.pose_output.size() != self.size():
            self.setFixedSize(self.pose_output.size())
        self.update()

class MainWindow(QWidget):
    def __init__(self, camera_index=0, fps=24):
        super().__init__()

        # threadpool setup for multi-threading:
        self.threadpool = QThreadPool()

        # set window size and video stream:
        self.mainStatus = False
        self.setFixedSize(900, 500)
        self.setWindowTitle('PhysicalQt')

        try:
            self.capture = cv2.VideoCapture(camera_index)
        except Exception as e:
            print("Error with getting webcamera feed!")

        # template load in:
        static_path = os.path.join(os.getcwd(), 'static')
        self.template_needstart = cv2.imread(os.path.join(static_path, 'template_needstart.png'))
        self.image = QLabel(self)
        self.image.setGeometry(QRect(35, 35, 450, 300))

        # set location
        self.image2 = QLabel(self)
        self.image2.setGeometry(QRect(550, 35, 300, 300))

        # load gt file manually here:
        self.gt_master, self.meta = gt.read_in_gt('../posenet/gt/jumping_jack/jumping_jack_02.json')

        # create main output feed:
        self.detectWidget = DetectionWidget(gt=self.gt_master[0])

        # load in other GUI elements:
        text = QLabel('webcam', self)
        text.setGeometry(QRect(35, 5, 50, 25))

        text = QLabel('motion', self)
        text.setGeometry(QRect(550, 5, 50, 25))

        self.status = False
        self.statusText = QLabel('Wrong movement detected', self)
        self.statusText.setGeometry(QRect(550,320,500,100))

        numText = QLabel('# of exercises done: 0', self)
        numText.setGeometry(QRect(550,300,600,100))

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

        # Add button and button functionality
        self.startb = QPushButton("Start Tracking", self)
        self.startb.setGeometry(QRect(50, 350, 150, 60))
        self.startb.clicked.connect(lambda: self.switch_on())

        self.end = QPushButton("Stop Tracking", self)
        self.end.setGeometry(QRect(200, 350, 150, 60))
        self.end.clicked.connect(lambda: self.switch_off())

        self.option_menu = QComboBox(self)
        self.options = ["jumping jack", "Jump Squat", "Lunge", "Star jumps", "Standing Side Stretch"]
        for op in self.options:
            self.option_menu.addItem(op)
        self.option_menu.setGeometry(QRect(350, 350, 150, 60))

        # timer to launch interactivity:
        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()

    def switch_on(self):
        self.mainStatus = 1

    def switch_off(self):
        self.mainStatus = 0

    def switch_status(self):
        self.mainStatus = not self.mainStatus

    def get_frame(self):
        _, frame = self.capture.read()
        img_viz = None
        if self.mainStatus:
            self.detectWidget.lastGoodFrame = (self.detectWidget.lastGoodFrame + 1) % self.meta[0]['meta']['total_frames']
            # img_viz -> output of everything being done
            img_viz = np.full((300,300, 3), 239, dtype=np.uint8)

            # ask threadpool to execute this a seperate thread:
            self.detectWidget.gen_output_pose(frame, img_viz)

            # ask threadpool to execute this as a seperate thread:
            # draw gt:
            #self.detectWidget.draw_gt(img_viz)
            gt_thread = threading.Thread(target=self.detectWidget.draw_gt, args=(img_viz,), daemon=True)
            gt_thread.start()

            # Continously check pose:
            for i in range(len(self.gt_master[0])):
                self.status = gt.evaluate(self.detectWidget.current_pose, self.gt_master[0][i])
                if self.status:
                    self.statusText.setText('Wrong movement detected')
                else:
                    self.statusText.setText('Correct movement detected') # add frames

        image = QImage(frame, *frame.shape[1::-1], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

        if self.mainStatus:
            pixmap = QPixmap.fromImage(get_qimage(img_viz))
            pixmap = pixmap.transformed(QTransform().scale(-1, 1))
            pixmap = pixmap.copy(QRect(155, 155, 250, 250))
            self.image2.setPixmap(pixmap)
            #self.image2.setPixmap(QPixmap.fromImage(get_qimage(img_viz)))
        else:
            self.image2.setPixmap(QPixmap.fromImage(get_qimage(self.template_needstart)))

        self.image2.setScaledContents(True)

    # destructor
    def __del__(self):
        print('free')
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
