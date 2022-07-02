import os
import re
import sys
import json
import pyqtgraph as pg
from ast import And
from turtle import home
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from database import userdbs
from video_thread import *
from threading import *
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QDesktopWidget

from random import randint
import urllib.request as ur


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("./ui/login.ui",self)
        self.db = userdbs()
        self.loginButton.clicked.connect(self.loginfunction)
        self.regButton.clicked.connect(self.gotocreate)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def loginfunction(self):
        self.error.setText("")
        email = self.email.text()
        password = self.password.text()
        if len(email)==0 or len(password)==0:
            self.error.setText("*Please input all fields.")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
        # print("Successfully logged in with email: ", email, "and password:", password)
            data = self.db.validate_username_pass(email,password)
            if data is not None:
                for pw in data:
                        if password == pw:
                            homepage=HomePage()
                            widget.addWidget(homepage)
                            widget.setCurrentIndex(widget.currentIndex()+1)
                            print("Successfully Logged in.")
                           
                        else:
                            self.error.setText("Incorrect password.")
            else:
                print("Incorrect username.")
                self.error.setText("Incorrect username.")

    def gotocreate(self):
        # self.db.close_connection()
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class HomePage(QDialog):
    def __init__(self):
        super(HomePage, self).__init__()
        widget.setFixedHeight(853)
        widget.setFixedWidth(1446)
        loadUi("./ui/home.ui",self)
        self.centerWin()
        self.db = userdbs()
        self.addPatient.clicked.connect(self.gotopatient)
        self.VBL = QVBoxLayout()
        self.saveTimer = QTimer()
        self.VBL.addWidget(self.videoFeed)
        self.feedStart.clicked.connect(self.controlTimer)
        self.CancelBTN.clicked.connect(self.PauseFeed)
        
        pnlist = self.db.pn_combo()
        pn_list = [i[0] for i in pnlist]
        self.patients_combo.addItems(pn_list)
        print(self.patients_combo.currentText())
        self.getDetails.pressed.connect(self.patientDetails)

    def centerWin(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.show()

    def patientDetails(self):
        p_name = self.patients_combo.currentText()
        patient_details = self.db.getPatientDetails(p_name)
        gest_age = patient_details[0][0]
        height = patient_details[0][1]
        weight = patient_details[0][2]
        self.p_name.setText("Name: "+p_name)
        self.p_age.setText("Gestational Age: "+str(gest_age))
        self.p_height.setText("Height: "+str(height))
        self.p_weight.setText("Weight: "+str(weight))

        #SpO2 Graph
        # self.x = list(range(100))  # 100 time points
        # self.y = [randint(0,100) for _ in range(100)]
        self.spo2_id=0
        self.a,self.b,self.spo2_id=self.get_json("1",self.spo2_id)
        self.spo2_graphWidget.setBackground('w')
        self.spo2_graphWidget.clear()
        pen = pg.mkPen(color=(255, 0, 0))
        self.spo2_graphWidget.plotItem.vb.setLimits(xMin=0, xMax=120, yMin=0, yMax=150)
        self.data_line1 =  self.spo2_graphWidget.plot(self.a, self.b, pen=pen)
        self.spo2.setText(str(self.b[-1]))
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(50)
        self.timer1.timeout.connect(self.update_plot_data1)
        self.timer1.start()

        #Heart Rate Graph
        # self.x = list(range(100))  # 100 time points
        # self.y = [randint(0,100) for _ in range(100)]
        self.heartrate_id=0
        self.c,self.d,self.heartrate_id=self.get_json("2",self.heartrate_id)
        self.hr_graphWidget.setBackground('w')
        self.hr_graphWidget.clear()
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line2 =  self.hr_graphWidget.plot(self.c, self.d, pen=pen)
        self.temp.setText(str(self.d[-1]))
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(50)
        self.timer2.timeout.connect(self.update_plot_data2)
        self.timer2.start()

        #Temp Rate Graph
        # self.x = list(range(100))  # 100 time points
        # self.y = [randint(0,100) for _ in range(100)]
        self.temprate_id=0
        self.e,self.f,self.temprate_id=self.get_json("3",self.temprate_id)
        self.temp_graphWidget.setBackground('w')
        self.temp_graphWidget.clear()
        pen = pg.mkPen(color=(255, 0, 0))
        self.temp_graphWidget.plotItem.vb.setLimits(xMin=0, xMax=120, yMin=0, yMax=300)
        self.data_line3 =  self.temp_graphWidget.plot(self.e, self.f, pen=pen)
        self.heartrate.setText(str(self.f[-1]))
        self.timer3 = QtCore.QTimer()
        self.timer3.setInterval(50)
        self.timer3.timeout.connect(self.update_plot_data3)
        self.timer3.start()

    def update_plot_data1(self):
        #print('reached1')
        temp_b,self.spo2_id=self.get_json("1",self.spo2_id)
        #print(temp_b)
        self.a.pop(0)  # Remove the first y element.
        self.a.append(self.a[-1] + 1)  # Add a new value 1 higher than the last.
        self.b.pop(0)  # Remove the first
        self.b.append(temp_b)  # Add a new random value.
        self.data_line1.setData(self.a, self.b)
        self.spo2.setText(str(self.b[-1]))
    
    def update_plot_data2(self):
        #print('reached2')
        temp_c,self.heartrate_id=self.get_json("2",self.heartrate_id)
        #print(temp_c)
        self.c.pop(0)  # Remove the first y element.
        self.c.append(self.c[-1] + 1)  # Add a new value 1 higher than the last.
        self.d.pop(0)  # Remove the first
        self.d.append(temp_c)  # Add a new random value.
        self.data_line2.setData(self.c, self.d)
        self.heartrate.setText(str(self.f[-1]))
        self.temp.setText(str(self.d[-1]))


    def update_plot_data3(self):
        #print('reached3')
        temp_d,self.temprate_id=self.get_json("3",self.temprate_id)
        #print(temp_d)
        self.e.pop(0)  # Remove the first y element.
        self.e.append(self.e[-1] + 1)  # Add a new value 1 higher than the last.
        self.f.pop(0)  # Remove the first
        self.f.append(temp_d)  # Add a new random value.
        self.data_line3.setData(self.e, self.f)

    def get_json(self,n,id):  
            res=[]
            url = "https://thingspeak.com/channels/1347725/field/"+n+".json"
            response = ur.urlopen(url)
            data =json.loads(response.read())
            data = data["feeds"]
            def sort_by_key(list):
                return list['entry_id']
            data=sorted(data, key=sort_by_key)
            if(id==0):
                data=data[:10]
                for x in data:
                    res.append(int(float(x["field"+n])))
                #print(res)
                return list(range(10)),res,data[9]['entry_id']+1
            for x in data:
                if(x['entry_id']==id):
                    return int(float(x["field"+n])),x['entry_id']+1

    def PauseFeed(self):
        if self.th2.active:
            self.th2.terminate()
            self.saveTimer.stop()

        #-----------------------------------------------------------------------------
    @QtCore.pyqtSlot(QImage)
    def setImage(self, Image):
        self.videoFeed.setPixmap(QPixmap.fromImage(Image))

    def controlTimer(self):
        
        if not self.saveTimer.isActive():
            # write video
            self.saveTimer.start()
            self.th2 = Thread2(self)
            self.th2.changePixmap.connect(self.setImage)
            self.th2.active = True                                
            self.th2.start()
                             
    
        #-----------------------------------------------------------------------------

    def gotopatient(self):
        # self.db.close_connection()
        createacc=PatientReg()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("./ui/user_reg.ui",self)
        self.regButton.clicked.connect(self.createaccfunction)
        self.cancelButton.clicked.connect(self.cancelUserReg)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password2.setEchoMode(QtWidgets.QLineEdit.Password)

    def cancelUserReg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Cancelled.")
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        msg.setText("User Registration Cancelled.")
        msg.exec_()

    def createaccfunction(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success.")

        name = self.name.text()
        affiliation = self.affiliation.text()
        number = self.number.text()
        username = self.username.text()
        email = self.email.text()
        password = self.password.text()
        password2 = self.password2.text()
        reg_details = {"name":name,"affiliation":affiliation,"username":username,"email":email,
                        "password":password,"number":number,"password2":password2}
        
        if(self.reg_validate(reg_details)):
            self.db = userdbs()
            self.db.registration(reg_details)
            self.db.close_connection()
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
            msg.setText("User Registration Successfull.")
            msg.exec_()

    def reg_validate(self,data):
        def email_validate(s):
            pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
            if re.match(pat,s):
                return True
            return False

        if len(data['name'])==0 or len(data['affiliation'])==0 or len(data['number'])==0 or len(data['username'])==0 or len(data['email'])==0 or len(data['password'])==0 or len(data['password2'])==0:
            print("Please fill in all inputs.")
            self.error.setText("*Please input all fields.")

        elif data['password']!=data['password2']:
            print("Passwords do not match.")
            self.error.setText("*Passwords do not match.")

        elif data['number'].isnumeric() == False:
            print("Please enter a valid phone number.")
            self.error.setText("*Please enter a valid phone number.")

        elif len(data['number']) != 10:
            print("Please enter a valid phone number.")
            self.error.setText("*Please enter a valid phone number.")

        elif email_validate(data['email']) == False:
            print("Invalid email address.")
            self.error.setText("*Please enter a valid email address.")

        else:
            return True

class PatientReg(QDialog):
    def __init__(self):
        super(PatientReg,self).__init__()
        loadUi("./ui/patient_reg.ui",self)
        self.db = userdbs()
        self.regButton.clicked.connect(self.patientreg)
        self.cancelButton.clicked.connect(self.cancelreg)
    
    def cancelreg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Cancelled.")
        homePage=HomePage()
        widget.addWidget(homePage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        msg.setText("patient Registration Cancelled.")
        msg.exec_()

    def patientreg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success.")

        name = self.name.text()
        gest_age = self.gest_age.text()
        height = self.height.text()
        weight = self.weight.text()
        init_obsv = self.init_obsv.text()
        roa = self.roa.text()
        reg_details = {"name":name,"gest_age":gest_age,"height":height,"weight":weight,
                        "init_obsv":init_obsv,"roa":roa}
        print(reg_details)
        if(self.patient_validate(reg_details)):
            self.db = userdbs()
            self.db.patient_reg(reg_details)
            self.db.close_connection()
            homePage=HomePage()
            widget.addWidget(homePage)
            widget.setCurrentIndex(widget.currentIndex()+1)
            msg.setText("patient Registration Successfull.")
            msg.exec_()

    def patient_validate(self, data):
        if len(data['name'])==0 or len(data['gest_age'])==0 or len(data['height'])==0 or len(data['weight'])==0 or len(data['init_obsv'])==0 or len(data['roa'])==0:
            print("Please fill in all inputs.")
            self.error.setText("*Please input all fields.")
        elif data['gest_age'].isnumeric() == False:
            print("Please enter the valid height.")
            self.error.setText("*Please enter the valid gestational age.")

        elif data['height'].isnumeric() == False:
            print("Please enter the valid height.")
            self.error.setText("*Please enter the valid height.")

        elif data['weight'].isnumeric() == False:
            print("Please enter the valid weight.")
            self.error.setText("*Please enter the valid weight.")

        else:
            return True

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setMinimumWidth(500)
widget.setMinimumHeight(600)
widget.show()
app.exec_()