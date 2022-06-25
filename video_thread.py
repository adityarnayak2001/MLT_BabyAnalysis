import sys
import cv2
import datetime
import pytz

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt5 import QtWidgets, QtCore, QtGui

class Thread1(QThread):
    changePixmap = pyqtSignal(QImage)
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.active = True

    def run(self):
        self.cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap1.set(3,480)
        self.cap1.set(4,640)
        self.cap1.set(5,30)
        while True:
            ret1, image1 = self.cap1.read()
            if ret1:
                im1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(im1, 1)
                height1, width1, channel1 = FlippedImage.shape
                step1 = channel1 * width1
                qImg1 = QImage(FlippedImage.data, width1, height1, step1, QImage.Format_RGB888)
                self.changePixmap.emit(qImg1)

class Thread2(QThread):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.active = True

    def run(self):
        if self.active:        
            current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            filename = "video_"+current_time.strftime("%m-%d_%H:%M:%S")+".avi"    
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID') 
            self.out1 = cv2.VideoWriter('Recordings/output.avi', self.fourcc, 30, (640,480))
            self.cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.cap1.set(3, 480)
            self.cap1.set(4, 640)
            self.cap1.set(5, 30)
            while self.active:                      
                ret1, image1 = self.cap1.read()
                if ret1:
                    self.out1.write(image1)     
                self.msleep(10)                      

    def stop(self):
        self.out1.release()