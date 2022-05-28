import sqlite3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Incorrect Username or Password")
            msg.setWindowTitle("Error")

            conn = sqlite3.connect("mlt.db")
            query = 'SELECT password FROM USERS WHERE username = \''+username+"\'"
            cur = conn.execute(query)
            user = cur.fetchone()
            if user is not None:
                for pw in user:
                    if password == pw:
                        print("Successfully Logged in.")
                        msg.setWindowTitle("Success.")
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Successfully Logged in.")
                        msg.exec_()
                    else:
                        print("Incorrect password.")
                        msg.setText("Incorrect Password")
                        msg.exec_()
            else:
                print("Incorrect username.")
                msg.setText("Incorrect Username")
                msg.exec_()
            
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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        
        name = self.name.text()
        affiliation = self.affiliation.text()
        number = self.number.text()
        username = self.username.text()
        email = self.email.text()
        password = self.password.text()
        password2 = self.password2.text()
        
        if len(name)==0 or len(affiliation)==0 or len(number)==0 or len(username)==0 or len(email)==0 or len(password)==0 or len(password2)==0:
            print("Please fill in all inputs.")
            msg.setText("Please fill in all inputs.")
            msg.exec_()

        elif password!=password2:
            print("Passwords do not match.")
            msg.setText("Passwords do not match.")
            msg.exec_()
        else:
            conn = sqlite3.connect("mlt.db")
            cur = conn.cursor()
            reg_details = [name, affiliation, number, email, username, password]
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