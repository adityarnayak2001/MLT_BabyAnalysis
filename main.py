import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
from database import userdbs

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginButton.clicked.connect(self.loginfunction)
        self.regButton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        print("Successfully logged in with email: ", email, "and password:", password)
        self.db = userdbs()
        flag = self.db.validate_username_pass(email,password)
        if flag:
            print("Login successful")
        #self.db.close_connection()

    def gotocreate(self):
        self.db.close_connection()
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("user_reg.ui",self)
        self.regButton.clicked.connect(self.createaccfunction)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        name = self.name.text()
        affiliation = self.affiliation.text()
        username = self.username.text()
        email = self.email.text()
        password = self.password.text()
        password2 = self.password2.text()
        reg_details = {"name":name,"affiliation":affiliation,"username":username,"email":email,
                        "password":password,"password2":password2}
        self.db = userdbs()
        self.db.registration(reg_details)
        # if self.password.text()==self.confirmpass.text():
        #     password=self.password.text()
        #    print("Successfully created acc with email: ", email, "and password: ", password)
            # login=Login()
            # widget.addWidget(login)
            # widget.setCurrentIndex(widget.currentIndex()+1)

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(500)
widget.setFixedHeight(600)
widget.show()
app.exec_()