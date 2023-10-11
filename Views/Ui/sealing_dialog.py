from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Repai_ro_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(340, 150)
        Dialog.setMinimumSize(QtCore.QSize(340, 150))
        Dialog.setMaximumSize(QtCore.QSize(340, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        Dialog.setFont(font)
        Dialog.setStyleSheet("background-color:white;")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(-1, 15, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:#464646;")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lbl_set_current_ro = QtWidgets.QLineEdit(Dialog)
        self.lbl_set_current_ro.setMinimumSize(QtCore.QSize(0, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_set_current_ro.setFont(font)
        self.lbl_set_current_ro.setStyleSheet("#lbl_set_current_ro{ border:1 solid #464646;  border-radius: 5px; background: #FFFFFF; color:#464646; padding: 0px 5px; }")
        self.lbl_set_current_ro.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_set_current_ro.setObjectName("lbl_set_current_ro")
        self.horizontalLayout.addWidget(self.lbl_set_current_ro)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lbl_range_current_ro = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_range_current_ro.setFont(font)
        self.lbl_range_current_ro.setStyleSheet("color:#464646;")
        self.lbl_range_current_ro.setObjectName("lbl_range_current_ro")
        self.verticalLayout.addWidget(self.lbl_range_current_ro)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_update_repair_ro = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_update_repair_ro.sizePolicy().hasHeightForWidth())
        self.btn_update_repair_ro.setSizePolicy(sizePolicy)
        self.btn_update_repair_ro.setMinimumSize(QtCore.QSize(100, 28))
        self.btn_update_repair_ro.setMaximumSize(QtCore.QSize(100, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_update_repair_ro.setFont(font)
        self.btn_update_repair_ro.setStyleSheet("#btn_update_repair_ro{ border:none; outline:none;  border-radius: 5px; background: #0072AD; color:#FFFFFF; padding: 0px 5px; }\n"
        "#btn_update_repair_ro:pressed { border-radius: 5px; outline:none; border:none; background: #216081; color:#FFFFFF ; padding: 0px 5px; }")
        self.btn_update_repair_ro.setObjectName("btn_update_repair_ro")
        self.horizontalLayout_2.addWidget(self.btn_update_repair_ro)
        self.btn_close_repair_ro = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_close_repair_ro.sizePolicy().hasHeightForWidth())
        self.btn_close_repair_ro.setSizePolicy(sizePolicy)
        self.btn_close_repair_ro.setMinimumSize(QtCore.QSize(100, 28))
        self.btn_close_repair_ro.setMaximumSize(QtCore.QSize(100, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_close_repair_ro.setFont(font)
        self.btn_close_repair_ro.setStyleSheet("#btn_close_repair_ro{ border:1 solid #0072AD; outline:none; border-radius: 5px; background: #FFFFFF; color:#0072AD; padding: 0px 5px; }\n"
        "#btn_close_repair_ro:pressed { border-radius: 5px; outline:none; border:none; background: #216081; color:#FFFFFF ; padding: 0px 5px; }")
        self.btn_close_repair_ro.setObjectName("btn_close_repair_ro")
        self.horizontalLayout_2.addWidget(self.btn_close_repair_ro)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sửa lệnh phát hành"))
        self.label.setText(_translate("Dialog", "Số hiện tại"))
        self.lbl_range_current_ro.setText(_translate("Dialog", "Số hiện tại có giá trị từ: "))
        self.btn_update_repair_ro.setText(_translate("Dialog", "Sửa"))
        self.btn_close_repair_ro.setText(_translate("Dialog", "Hủy"))

class RepairRo(QtWidgets.QDialog):
                    
    def __init__(self, *args, **kwargs):
        """SignIn constructor."""
        super().__init__(*args, **kwargs)
        self.ui = Ui_Repai_ro_Dialog()
        self.ui.setupUi(self)

        self.id_ro      = None
        self.start_ro   = None
        self.end_ro     = None
        self.current_ro = None
        self.lang       = None

        self.ui.btn_close_repair_ro.clicked.connect(self.slot_btn_close_repair_ro)
        self.ui.btn_update_repair_ro.clicked.connect(self.slot_btn_update_repair_ro)
        # Connects the function that inputs data for sign in to the OK button.
        # self.ui.signin_buttonBox.accepted.connect(self.sign_in_authenticate)

    def draw(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", self.lang['Dialog'] + self.id_ro))
        self.ui.lbl_set_current_ro.setText(self.current_ro)
        self.ui.lbl_range_current_ro.setText(self.lang['lbl_range_current_ro'] + self.start_ro + " - " + self.end_ro)
        self.ui.label.setText(_translate("Dialog", self.lang['label']))
        self.ui.btn_update_repair_ro.setText(_translate("Dialog", self.lang['btn_update_repair_ro']))
        self.ui.btn_close_repair_ro.setText(_translate("Dialog", self.lang['btn_close_repair_ro']))

    def slot_btn_close_repair_ro(self):
        self.reject()
    
    def slot_btn_update_repair_ro(self):
        input_text = self.ui.lbl_set_current_ro.text()
            
        if input_text == "":
            QtWidgets.QMessageBox.critical(self, self.lang['note'], self.lang['message_1'])
        else:
            try: 
                input_current = int(input_text)
            except:
                QtWidgets.QMessageBox.critical(self,self.lang['note'], self.lang['message_2'])
            else:
                if input_current < int(self.start_ro) or input_current > int(self.end_ro):
                    QtWidgets.QMessageBox.critical(self,self.lang['note'], self.lang['message_3'])
                else:
                    self.current_ro = self.ui.lbl_set_current_ro.text()

                    self.accept()