from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")      
        MainWindow.resize(640, 480)     
        self.centralwidget = QWidget(MainWindow)      
        self.centralwidget.setObjectName("centralwidget")   
        self.label = QLabel(self.centralwidget)   
        self.label.setGeometry(QRect(10, 10, 500, 300))  
        self.label.setText("")  
        self.label.setObjectName("label")   
        self.pushButton = QPushButton(self.centralwidget) 
        self.pushButton.setGeometry(QRect(50, 400, 75, 23))  
        self.pushButton.setObjectName("pushButton") 
        MainWindow.setCentralWidget(self.centralwidget) 
        self.statusbar = QStatusBar(MainWindow)   
        self.statusbar.setObjectName("statusbar")   
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.play)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))


    def play(self):     
        cap = cv2.VideoCapture(0)
        while True:
            ret, show = cap.read()
            key = cv2.waitKey(1) & 0xFF
            if ret:
                rgbImage = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
                image = QImage(rgbImage.data, show.shape[1], show.shape[0], show.strides[0], QImage.Format_RGB888)
                l = self.label.setPixmap(QPixmap.fromImage(image).scaled(500, 300, Qt.IgnoreAspectRatio))
            if key == ord('p'):
                cv2.waitKey(0)

            elif key == ord('q'):
                break


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())