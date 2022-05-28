import sqlite3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi    

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginButton.clicked.connect(self.gotologin)
        self.regButton.clicked.connect(self.gotocreate)

    def gotologin(self):
        username = self.username.text()
        password = self.password.text()
        #print("Successfully logged in with email: ", email, "and password:", password)
        if len(username)==0 or len(password)==0:
            self.error.setText("Please input all fields.")
        else:
            conn = sqlite3.connect("mlt.db")
            cur = conn.cursor()
            query = 'SELECT password FROM USERS WHERE username = \''+username+"\'"
            cur.execute(query)
            #result_pass = cur.fetchone()
            query_result = cur.fetchone()[0]
            if query_result is not None:
                print("Successfully logged in.")
                print(query_result)
            else:
                print("Invalid username or password.")

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("user_reg.ui",self)
        self.regButton.clicked.connect(self.createaccfunction)
        #self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        #self.password2.setEchoMode(QtWidgets.QLineEdit.Password2)

    def createaccfunction(self):
        name = self.name.text()
        affiliation = self.affiliation.text()
        username = self.username.text()
        email = self.email.text()
        password = self.password.text()
        password2 = self.password2.text()
        
        if len(name)==0 or len(affiliation)==0 or len(username)==0 or len(email)==0 or len(password)==0 or len(password2)==0:
            self.error.setText("Please fill in all inputs.")

        elif password!=password2:
            self.error.setText("Passwords do not match.")
        else:
            conn = sqlite3.connect("mlt.db")
            cur = conn.cursor()
            reg_details = [name, affiliation, username, email, password, password2]
            cur.execute("INSERT INTO USERS ('name','affiliation','number','email','username','password') VALUES" 
        +"(?,?,?,?,?,?)",reg_details)
            conn.commit()
            conn.close()
            loginPage = Login()
            widget.addWidget(loginPage)
            widget.setCurrentIndex(widget.currentIndex()+1)

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(500)
widget.setFixedHeight(600)
widget.show()
app.exec_()