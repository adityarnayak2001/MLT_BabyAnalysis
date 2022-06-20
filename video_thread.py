import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import datetime
import pytz


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        #self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        frame_width = int(Capture.get(3))
        frame_height = int(Capture.get(4))
        filename = "".join(["outpy_",current_time.strftime("%Y-%m-%d_%H:%M:%S"),".avi"])
        #filename = "outpy_"+current_time.strftime("%Y-%m-%d_%H:%M:%S")+".avi"
        #print(filename)
        out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

        while(True):
            ret, frame = Capture.read()
            if ret:
                out.write(frame)
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                

    def pause(self):
        #self.ThreadActive = True
        Capture1 = cv2.VideoCapture(0)
        while(True):
            ret, frame = Capture1.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow('frame', Image)
                cv2.waitKey(1)