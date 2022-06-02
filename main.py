from ast import And
import re
import sys
from turtle import home
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
from database import userdbs

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.db = userdbs()
        self.loginButton.clicked.connect(self.loginfunction)
        self.regButton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        self.error.setText("")
        email = self.email.text()
        password = self.password.text()
        if len(email)==0 or len(password)==0:
            self.error.setText("Please input all fields.")
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

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("user_reg.ui",self)
        self.regButton.clicked.connect(self.createaccfunction)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

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
            self.error.setText("Please input all fields.")

        elif data['password']!=data['password2']:
            print("Passwords do not match.")
            self.error.setText("Passwords do not match.")

        elif data['number'].isnumeric() == False:
            print("Please enter a valid phone number.")
            self.error.setText("Please enter a valid phone number.")

        elif len(data['number']) != 10:
            print("Please enter a valid phone number.")
            self.error.setText("Please enter a valid phone number.")

        elif email_validate(data['email']) == False:
            print("Invalid email address.")
            self.error.setText("Please enter a valid email address.")

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