import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pyrebase
import firebase_admin
from firebase_admin import db

firebaseConfig={'apiKey':"AIzaSyB9eMHhNxSrGvwI6NZ2hFUqA8rc0zbkwC4",
'authDomain':"pltmlbabyanalysis.firebaseapp.com",
'projectId':"pltmlbabyanalysis",
'storageBucket':"pltmlbabyanalysis.appspot.com",
'messagingSenderId':"283761884299",
'appId':"1:283761884299:web:0c804922739d061c4be88e",
'measurementId':"G-YPQSFGV2F8"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

ref = db.reference("/")

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginButton.clicked.connect(self.loginfunction)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        print("Successfully logged in with email: ", email, "and password:", password)

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(500)
widget.setFixedHeight(600)
widget.show()
app.exec_()