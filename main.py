from ast import And
import re
import sys
from turtle import home
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
from database import userdbs
from video_thread import *
from threading import *

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
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
                            #msg.setWindowTitle("Success.")
                            #msg.setIcon(QMessageBox.Information)
                            #msg.setText("Successfully Logged in.")
                            #msg.exec_()
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
        loadUi("home.ui",self)
        self.db = userdbs()
        self.addPatient.clicked.connect(self.gotopatient)
        self.VBL = QVBoxLayout()
        self.VBL.addWidget(self.videoFeed)
        self.feedStart.clicked.connect(self.thread)
        self.CancelBTN.clicked.connect(self.PauseFeed)
        pnlist = self.db.pn_combo()
        pn_list = [i[0] for i in pnlist]
        self.patients_combo.addItems(pn_list)
        print(self.patients_combo.currentText())
        self.getDetails.pressed.connect(self.patientDetails)

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

    def ImageUpdateSlot(self, Image):
        self.videoFeed.setPixmap(QPixmap.fromImage(Image))

    def thread(self):
        t1 = Thread(target=self.startFeed)
        t1.start()

    def startFeed(self):
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def PauseFeed(self):
        self._running = False
        homePage=HomePage()
        widget.addWidget(homePage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotopatient(self):
        # self.db.close_connection()
        createacc=PatientReg()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("user_reg.ui",self)
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
        loadUi("patient_reg.ui",self)
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