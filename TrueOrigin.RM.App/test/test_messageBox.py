
import sys
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtCore as qtc 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore, QtGui, QtWidgets                                 # +++


#from mainwindow import Ui_MainWindow
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(311, 293)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.signin_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.signin_pushButton.setGeometry(QtCore.QRect(100, 110, 89, 25))
        self.signin_pushButton.setObjectName("signin_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 311, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.signin_pushButton.setText(_translate("MainWindow", "Sign in "))
        
        
#from dialog import Ui_signin_Dialog
class Ui_signin_Dialog(object):
    def setupUi(self, signin_Dialog):
        signin_Dialog.setObjectName("signin_Dialog")
        signin_Dialog.resize(400, 300)
        self.signin_buttonBox = QtWidgets.QDialogButtonBox(signin_Dialog)
        self.signin_buttonBox.setGeometry(QtCore.QRect(290, 230, 80, 56))
        self.signin_buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.signin_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.signin_buttonBox.setObjectName("signin_buttonBox")
        self.input_lineEdit = QtWidgets.QLineEdit(signin_Dialog)
        self.input_lineEdit.setGeometry(QtCore.QRect(140, 130, 113, 25))
        self.input_lineEdit.setObjectName("input_lineEdit")

        self.retranslateUi(signin_Dialog)
#        self.signin_buttonBox.accepted.connect(signin_Dialog.accept)           # ---
        self.signin_buttonBox.rejected.connect(signin_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(signin_Dialog)

    def retranslateUi(self, signin_Dialog):
        _translate = QtCore.QCoreApplication.translate
        signin_Dialog.setWindowTitle(_translate("signin_Dialog", "Dialog"))
        

class SignIn(qtw.QDialog):

    def __init__(self, *args, **kwargs):
        """SignIn constructor."""
        super().__init__(*args, **kwargs)
        self.ui = Ui_signin_Dialog()
        self.ui.setupUi(self)

        # Connects the function that inputs data for sign in to the OK button.
        self.ui.signin_buttonBox.accepted.connect(self.sign_in_authenticate)

    def sign_in_authenticate(self):
        input_text = self.ui.input_lineEdit.text()
        
        if input_text == "":
            qtw.QMessageBox.critical(self,"Note", "Please input your data.")
        else:                                                                   # +++
            self.accept()                                                       # +++


class FirstPage(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        """FirstPage constructor."""
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connecting the buttons to open Sign in and Sign out pages
        self.ui.signin_pushButton.clicked.connect(self.open_sign_in_page)

        self.show()

    def open_sign_in_page(self):
        self.sigin = SignIn()
        self.sigin.show()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = FirstPage()
    sys.exit(app.exec_())