from tracemalloc import start
import Views.Ui.Image
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QDateTime
from GPIO.DefineParameter import ParaMachine
from Features.Worker import Worker

import enumerate.enum_init as enum

import requests
import json

from PyQt5.QtCore import *
import sys, os, inspect

import Views.Ui.sealing_gui as seal
import Views.Ui.sealing_dialog as dialog
import Views.sealing_string as sstring

from Libraries.LibHandling import LibHandling, ResultLogin, MachineFunc
from Database.DQD_EntityFrameworkCore.Repository.VariableRepository import VariableRepository


class ViewHandling(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        """SignIn constructor."""
        super().__init__(*args, **kwargs)
        self.ui = seal.Ui_MainWindow()
        self.variableRepository = VariableRepository()
        self.ss = sstring.Sealing_string()

        self.ui.setupUi(self)
        self.retranslateUi(self)

        self.Library = LibHandling()

        self.ui.stackwget_main.setCurrentIndex(1)

    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(
                        self, 'Confirm Close', 'Are you sure you want to close the app?',
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            print("CLOSE APP")
            os.system("killall python3")
            event.accept()
        else:
            event.ignore()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Máy phát hành iSeal"))
        MainWindow.setWindowIcon(QtGui.QIcon('image/logo.png'))
        self.ui.label_7.setText(_translate("MainWindow", "Seri thiết lập:"))
        self.ui.btn_sealing_manual.setText(_translate("MainWindow", "Phát hành"))
        self.ui.label_13.setText(_translate("MainWindow", "Tiến trình:"))
        self.ui.btn_return_setup.setText(_translate("MainWindow", "Quay lại"))
        self.ui.label_12.setText(_translate("MainWindow", "MÁY PHÁT HÀNH TEM iSEAL"))
        self.ui.label_3.setText(_translate("MainWindow", "ĐĂNG NHẬP"))
        self.ui.label_8.setText(_translate("MainWindow", "Tên đăng nhập:"))
        self.ui.txt_username.setPlaceholderText(_translate("MainWindow", "Tên đăng nhập"))
        self.ui.label_9.setText(_translate("MainWindow", "Mật khẩu:"))
        self.ui.txt_password.setPlaceholderText(_translate("MainWindow", "Nhập mật khẩu"))
        self.ui.btn_login.setText(_translate("MainWindow", "Đăng nhập"))
        self.ui.btn_setup.setText(_translate("MainWindow", " Thiết lập"))
        self.ui.lbl_username.setText(_translate("MainWindow", "Tên tài khoản"))
        self.ui.btn_logout.setText(_translate("MainWindow", " Đăng xuất"))
        self.ui.lbl_ro_selected.setText(_translate("MainWindow", "Lệnh đang thực hiện: Chưa xác định"))
        self.ui.label_2.setText(_translate("MainWindow", "Danh sách lệnh phát hành"))
        self.ui.label.setText(_translate("MainWindow", "Thông tin lệnh phát hành: "))
        self.ui.rtb_detail_ro.setPlaceholderText(_translate("MainWindow", "Thông tin chi tiết"))
        self.ui.btn_refresh_orders.setText(_translate("MainWindow", "Chuyển lệnh"))
        self.ui.btn_select.setText(_translate("MainWindow", " Chọn "))
        self.ui.rtb_info_ro_selected.setPlaceholderText(_translate("MainWindow", "Thông tinh lệnh phát hành"))
        self.ui.label_14.setText(_translate("MainWindow", "Số lượng thành công:"))
        self.ui.btn_detail_success.setText(_translate("MainWindow", "Danh sách chi tiết"))
        self.ui.lbl_num_success.setText(_translate("MainWindow", "0"))
        self.ui.label_16.setText(_translate("MainWindow", "Số lượng thất bại:"))
        self.ui.lbl_num_fail.setText(_translate("MainWindow", "0"))
        self.ui.label_17.setText(_translate("MainWindow", "Số seri đang phát hành:"))
        self.ui.lbl_numberSeri.setText(_translate("MainWindow", "12212121112"))
        self.ui.label_18.setText(_translate("MainWindow", "Tổng số đã phát hành: "))
        self.ui.lbl_total_success.setText(_translate("MainWindow", "300000/1000000"))
        self.ui.label_19.setText(_translate("MainWindow", "Tiến trình:"))
        self.ui.rtb_progress_release.setPlaceholderText(_translate("MainWindow", "Thông tinh lệnh phát hành"))
        self.ui.btn_return.setText(_translate("MainWindow", "  Quay lại"))
        self.ui.btn_start.setText(_translate("MainWindow", " Bắt đầu "))
        # self.ui.btn_emergency.setText(_translate("MainWindow", " Dừng "))
        self.ui.label_6.setText(_translate("MainWindow", "Danh sách tem thành công"))
        self.ui.btn_close.setText(_translate("MainWindow", "   Đóng"))
        self.ui.actionExit.setText(_translate("MainWindow", "Exit"))
        self.ui.label_4.setText(_translate("MainWindow", "Trạng thái hệ thống:"))
        self.ui.btn_status_display.setText(_translate("MainWindow", "   Đang hoạt động"))
        self.ui.btn_repair_ro.setText(_translate("MainWindow", "Sửa lệnh phát hành"))

        item = self.ui.table_releaser_order.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.ui.table_releaser_order.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Tổng"))
        item = self.ui.table_releaser_order.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Bắt đầu"))
        item = self.ui.table_releaser_order.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Hiện tại"))
        item = self.ui.table_releaser_order.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Trạng thái"))

        item = self.ui.table_list_istamp.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "STT"))
        item = self.ui.table_list_istamp.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Số index"))
        item = self.ui.table_list_istamp.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Số seri"))
        item = self.ui.table_list_istamp.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Thời gian"))
        item = self.ui.table_list_istamp.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "ID lệnh"))

        self.ui.txt_username.setText(_translate("MainWindow", "chungnn@stech.vn"))
        self.ui.txt_password.setText(_translate("MainWindow", "stechqman123"))

        self.ui.label_5.setText(_translate("MainWindow", "Thiết lập"))
        self.ui.lbl_setup_name.setText(_translate("MainWindow", "Tên đăng nhập"))
        self.ui.btn_setup_info.setText(_translate("MainWindow", "     Thông tin tài khoản"))
        self.ui.btn_setup_lang.setText(_translate("MainWindow", "     Ngôn ngữ"))
        self.ui.label_10.setText(_translate("MainWindow", "Tên tài khoản:"))
        self.ui.label_15.setText(_translate("MainWindow", "Email:"))
        self.ui.label_20.setText(_translate("MainWindow", "Giới tính:"))
        self.ui.radioButton.setText(_translate("MainWindow", "Tiếng Việt"))
        self.ui.radioButton_2.setText(_translate("MainWindow", "English"))
        self.ui.btn_setup_return.setText(_translate("MainWindow", "Quay lại"))

    def button_setEnable(self, btn, enable, text=None):
        btn_name = btn.objectName()
        if enable == True:
            if btn_name == 'btn_select':
                self.ui.btn_select.setEnabled(True)
                self.ui.btn_select.setStyleSheet("#btn_select { border:none;outline: none; border-radius: 8px; background: #0072AD; color:#FFFFFF; padding: 0px 5px; }"
                                            "#btn_select:pressed { border-radius: 8px; border:none; background: #216081; color:#FFFFFF ; padding: 0px 5px; }" )
            if btn_name == 'btn_format_select':
                self.ui.btn_format_select.setEnabled(True)
                self.ui.btn_format_select.setStyleSheet("#btn_format_select { border:none;outline: none; border-radius: 8px; background: #0072AD; color:#FFFFFF; padding: 0px 5px; }"
                                            "#btn_format_select:pressed { border-radius: 8px; border:none; background: #216081; color:#FFFFFF ; padding: 0px 5px; }" )
            elif btn_name == 'btn_refresh_orders':
                self.ui.btn_refresh_orders.setEnabled(True)
                self.ui.btn_refresh_orders.setStyleSheet("#btn_refresh_orders{ border:1 solid #0072AD; outline: none;border-radius: 8px; background: #FFFFFF; color:#0072AD; padding: 0px 5px; }"
                                            "#btn_refresh_orders:pressed { border-radius: 8px; border:none; outline: none;background: #216081; color:#FFFFFF ; padding: 0px 5px; }" )
            elif btn_name == 'btn_return':
                self.ui.btn_return.setEnabled(True)
                self.ui.btn_return.setStyleSheet("#btn_return{ border:none;outline: none; border-radius: 5px; background: #0072AD; color:#FFFFFF; padding: 0px 5px; }"
                                            "#btn_return:pressed{ border-radius: 5px; border:none; background: #216081; color:#FFFFFF ; padding: 0px 5px; }" )
            elif btn_name == 'btn_start':
                self.ui.btn_start.setEnabled(True)
                if text == self.lang['status_bt']['PAUSE']:
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/icon_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.ui.btn_start.setIcon(icon)
                    self.ui.btn_start.setStyleSheet("#btn_start{ border:none;outline: none; border-radius: 5px; background: #FFD233; color:#FFFFFF; padding: 0px 5px; }"
                                            "#btn_start:pressed { border-radius: 5px; border:none; background: #D0AB28; color:#FFFFFF ; padding: 0px 5px; }" )
                elif text == self.lang['status_bt']['START']:
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/icon_start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.ui.btn_start.setIcon(icon)
                    self.ui.btn_start.setStyleSheet("#btn_start{ border:none;outline: none; border-radius: 5px; background: #19DD73; color:#FFFFFF; padding: 0px 5px; }"
                                                "#btn_start:pressed { border-radius: 5px; border:none; background: #14A255; color:#FFFFFF ; padding: 0px 5px; }" )                            
                self.ui.btn_start.setText(text)
            elif btn_name == 'btn_logout':
                self.ui.btn_logout.setEnabled(True)
                self.ui.btn_logout.setStyleSheet("#btn_logout{ border:none;outline: none; border-radius: 5px; background: #0072AD; color:#FFFFFF; padding: 0px 5px; }"
                                            "#btn_logout:pressed { border-radius: 5px; border:none; background: #216081; color:#FFFFFF ; padding: 0px 5px; }")
            elif btn_name == 'btn_sync_ro_manual':
                self.ui.btn_sync_ro_manual.setVisible(True)
                self.ui.btn_sync_ro_manual.setText(text)
            
            elif btn_name == 'btn_repair_ro':
                self.ui.btn_repair_ro.setVisible(True)

        else:
            if btn_name == 'btn_select':
                self.ui.btn_select.setEnabled(False)
                self.ui.btn_select.setStyleSheet("#btn_select { border:none;outline: none; border-radius: 8px; background: #A8A8A8; color:#FFFFFF; padding: 0px 5px; }")
            if btn_name == 'btn_format_select':
                self.ui.btn_format_select.setEnabled(False)
                self.ui.btn_format_select.setStyleSheet("#btn_format_select { border:none;outline: none; border-radius: 8px; background: #A8A8A8; color:#FFFFFF; padding: 0px 5px; }")
            elif btn_name == 'btn_refresh_orders':
                self.ui.btn_refresh_orders.setEnabled(False)
                self.ui.btn_refresh_orders.setStyleSheet("#btn_refresh_orders { border:none;outline: none; border-radius: 8px; background: #A8A8A8; color:#FFFFFF; padding: 0px 5px; }")
            elif btn_name == 'btn_return':
                self.ui.btn_return.setEnabled(False)
                self.ui.btn_return.setStyleSheet("#btn_return { border:none;outline: none; border-radius: 8px; background: #A8A8A8; color:#FFFFFF; padding: 0px 5px; }")
            elif btn_name == 'btn_start':
                self.ui.btn_start.setEnabled(False)
                if text == self.lang['status_bt']['PAUSE']:
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/icon_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.ui.btn_start.setIcon(icon)
                    self.ui.btn_start.setStyleSheet("#btn_start{ border:none;outline: none; border-radius: 5px; background: #A8A8A8; color:#FFFFFF; padding: 0px 5px; }")
                elif text == self.lang['status_bt']['START']:
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/icon_start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.ui.btn_start.setIcon(icon)
                    self.ui.btn_start.setStyleSheet("#btn_start{ border:none;outline: none; border-radius: 5px; background: #A8A8A8; color:#FFFFFF; padding: 0px 5px; }") 
                self.ui.btn_start.setText(text)
            elif btn_name == 'btn_logout':
                self.ui.btn_logout.setEnabled(False)
                self.ui.btn_logout.setStyleSheet("#btn_logout { border:none;outline: none; border-radius: 5px; background: #A8A8A8; color:#FFFFFF; padding: 0px 5px; }")
            elif btn_name == 'btn_sync_ro_manual':
                self.ui.btn_sync_ro_manual.setVisible(False)

            elif btn_name == 'btn_repair_ro':
                self.ui.btn_repair_ro.setVisible(False)
            elif btn_name == 'btn_compelte':
                self.ui.btn_start.setEnabled(False)
                self.ui.btn_start.setStyleSheet("#btn_start { border:none;outline: none; border-radius: 5px; background: #A8A8A8; color:#FFFFFF; padding: 0px 5px; }")

    def button_setStatus(self, status, string_text):
        icon = QtGui.QIcon()
        if status == 'INIT':
            icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/s_init.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.btn_status_display.setStyleSheet("#btn_status_display{ border:1 solid #B9B9B9; outline: none; border-radius: 5px; background: #FFFFFF; color:#464646; padding: 0px 5px;}")
        elif status == 'READY':
            icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/s_ready.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.btn_status_display.setStyleSheet("#btn_status_display{ border:1 solid #B9B9B9; outline: none; border-radius: 5px; background: #FFFFFF; color:#19DD73; padding: 0px 5px;}")
        elif status == 'RELEASING':
            icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/s_releasing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.btn_status_display.setStyleSheet("#btn_status_display{ border:1 solid #B9B9B9; outline: none; border-radius: 5px; background: #FFFFFF; color:#0072AD; padding: 0px 5px;}")
        elif status == 'PAUSE':
            icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/s_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.btn_status_display.setStyleSheet("#btn_status_display{ border:1 solid #B9B9B9; outline: none; border-radius: 5px; background: #FFFFFF; color:#FFD233; padding: 0px 5px;}")
        elif status == 'STOP':
            icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/s_STOP.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.btn_status_display.setStyleSheet("#btn_status_display{ border:1 solid #B9B9B9; outline: none; border-radius: 5px; background: #FFFFFF; color:#F63838; padding: 0px 5px;}")
        elif status == 'COMPLETE':
            icon.addPixmap(QtGui.QPixmap(":/newPrefix/image/s_complete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.btn_status_display.setStyleSheet("#btn_status_display{ border:1 solid #B9B9B9; outline: none; border-radius: 5px; background: #FFFFFF; color:#6418C3; padding: 0px 5px;}")

        self.ui.btn_status_display.setIcon(icon)
        self.ui.btn_status_display.setText(string_text)

    def ini_lang_gui(self): 
        _translate = QtCore.QCoreApplication.translate
        self.ui.label_7.setText(_translate("MainWindow", self.lang['gui']['label_7']))
        self.ui.btn_sealing_manual.setText(_translate("MainWindow", self.lang['gui']['btn_sealing_manual']))
        self.ui.label_13.setText(_translate("MainWindow", self.lang['gui']['label_13']))
        self.ui.btn_return_setup.setText(_translate("MainWindow", self.lang['gui']['btn_return_setup']))
        self.ui.label_12.setText(_translate("MainWindow", self.lang['gui']['label_12']))
        self.ui.label_3.setText(_translate("MainWindow", self.lang['gui']['label_3']))
        self.ui.label_8.setText(_translate("MainWindow", self.lang['gui']['label_8']))
        self.ui.txt_username.setPlaceholderText(_translate("MainWindow", self.lang['gui']['txt_username']))
        self.ui.label_9.setText(_translate("MainWindow", self.lang['gui']['label_9']))
        self.ui.txt_password.setPlaceholderText(_translate("MainWindow", self.lang['gui']['txt_password']))
        self.ui.btn_login.setText(_translate("MainWindow", self.lang['gui']['btn_login']))
        self.ui.btn_setup.setText(_translate("MainWindow", self.lang['gui']['btn_setup']))
        try:
            self.ui.lbl_username.setText(self.lang['gui']['lbl_username'] + self.user_login[enum.iUser.NAME.value] + " ")
        except:
            self.ui.lbl_username.setText(_translate("MainWindow", self.lang['gui']['lbl_username']))
        self.ui.btn_logout.setText(_translate("MainWindow",self.lang['gui']['btn_logout']))
        self.ui.lbl_ro_selected.setText(_translate("MainWindow", self.lang['gui']['lbl_ro_selected']))
        self.ui.label_2.setText(_translate("MainWindow", self.lang['gui']['label_2']))
        self.ui.label.setText(_translate("MainWindow", self.lang['gui']['label']))
        self.ui.rtb_detail_ro.setPlaceholderText(_translate("MainWindow", self.lang['gui']['rtb_detail_ro']))
        self.ui.btn_refresh_orders.setText(_translate("MainWindow", self.lang['gui']['btn_refresh_orders']))
        self.ui.btn_select.setText(_translate("MainWindow", self.lang['gui']['btn_select']))
        self.ui.rtb_info_ro_selected.setPlaceholderText(_translate("MainWindow", self.lang['gui']['rtb_info_ro_selected']))
        self.ui.label_14.setText(_translate("MainWindow", self.lang['gui']['label_14']))
        self.ui.btn_detail_success.setText(_translate("MainWindow", self.lang['gui']['btn_detail_success']))
        self.ui.label_16.setText(_translate("MainWindow", self.lang['gui']['label_16']))
        self.ui.label_17.setText(_translate("MainWindow", self.lang['gui']['label_17']))
        self.ui.label_18.setText(_translate("MainWindow", self.lang['gui']['label_18']))
        self.ui.label_19.setText(_translate("MainWindow", self.lang['gui']['label_19']))
        self.ui.rtb_progress_release.setPlaceholderText(_translate("MainWindow", self.lang['gui']['rtb_progress_release']))
        self.ui.label_6.setText(_translate("MainWindow", self.lang['gui']['label_6']))
        self.ui.label_4.setText(_translate("MainWindow", self.lang['gui']['label_4']))
        self.ui.btn_repair_ro.setText(_translate("MainWindow", self.lang['gui']['btn_repair_ro']))
        self.ui.btn_return.setText(_translate("MainWindow", self.lang['status_bt']['RETURN']))
        self.ui.btn_close.setText(_translate("MainWindow", self.lang['gui']['btn_close']))

        item = self.ui.table_releaser_order.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", self.lang['gui']['table_releaser_order0']))
        item = self.ui.table_releaser_order.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", self.lang['gui']['table_releaser_order1']))
        item = self.ui.table_releaser_order.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", self.lang['gui']['table_releaser_order2']))
        item = self.ui.table_releaser_order.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", self.lang['gui']['table_releaser_order3']))
        item = self.ui.table_releaser_order.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", self.lang['gui']['table_releaser_order4']))

        item = self.ui.table_list_istamp.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", self.lang['gui']['table_list_istamp0']))
        item = self.ui.table_list_istamp.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", self.lang['gui']['table_list_istamp1']))
        item = self.ui.table_list_istamp.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", self.lang['gui']['table_list_istamp2']))
        item = self.ui.table_list_istamp.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", self.lang['gui']['table_list_istamp3']))
        item = self.ui.table_list_istamp.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", self.lang['gui']['table_list_istamp4']))

        self.ui.label_5.setText(_translate("MainWindow", self.lang['gui']['label_5']))
        self.ui.btn_setup_info.setText(_translate("MainWindow", self.lang['gui']['btn_setup_info']))
        self.ui.btn_setup_lang.setText(_translate("MainWindow", self.lang['gui']['btn_setup_lang']))
        self.ui.btn_setup_stamp.setText(_translate("MainWindow", self.lang['gui']['btn_setup_stamp']))
        self.ui.label_10.setText(_translate("MainWindow", self.lang['gui']['label_10']))
        self.ui.label_15.setText(_translate("MainWindow", self.lang['gui']['label_15']))
        self.ui.label_20.setText(_translate("MainWindow", self.lang['gui']['label_20']))
        self.ui.label_21.setText(_translate("MainWindow", self.lang['gui']['label_21']))
        self.ui.label_22.setText(_translate("MainWindow", self.lang['gui']['label_22']))
        self.ui.label_23.setText(_translate("MainWindow", self.lang['gui']['label_23']))
        self.ui.label_27.setText(_translate("MainWindow", self.lang['gui']['label_27']))
        self.ui.label_28.setText(_translate("MainWindow", self.lang['gui']['label_28']))
        self.ui.btn_setup_return.setText(_translate("MainWindow", self.lang['gui']['btn_setup_return']))

    def ini_lang_sys(self, lang):
        cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"sealing_lang.json")))
        if cmd_subfolder not in sys.path:
            sys.path.insert(0, cmd_subfolder)

        f = open(cmd_subfolder, encoding='utf-8')
        data = json.load(f)
        self.lang = data['lang'][lang]
        if(lang == 'vi'):
            self.ui.radioButton.setChecked(True)
        else:
            self.ui.radioButton_2.setChecked(True)
        f.close()

        self.ini_lang_gui()
        self.statusRO.clear()
        self.statusRO.append(self.lang['status_ro']['APPROVING'])
        self.statusRO.append(self.lang['status_ro']['DISABLE'])
        self.statusRO.append(self.lang['status_ro']['READY'])
        self.statusRO.append(self.lang['status_ro']['RELEASING'])
        self.statusRO.append(self.lang['status_ro']['COMPLETE'])
        self.statusRO.append(self.lang['status_ro']['STOP'])
        self.statusRO.append(self.lang['status_ro']['PAUSE'])

    def slot_btn_login(self):
        self.ui.lbl_message_login.setText('')

        username = self.ui.txt_username.text()
        password = self.ui.txt_password.text()

        # try:
        if ParaMachine.RUN_OFFLINE.value == True:
            self.ui.stackwget_main.setCurrentIndex(2)
            self.ui.stackwget_action.setCurrentIndex(0)

            self.user_login.clear()
            self.user_login.append(23)
            self.user_login.append("releaser2")
            self.user_login.append("releaser2@gmail.com")

            self.list_ro = ParaMachine.RELEASE_ORDER_EMULATOR.value
        else:
            login = self.Library.Login(username, password) # ĐĂNG NHẠP với server
            if login[0] == ResultLogin.LoginSuccess: #Nếu đăng nhập thành công
                self.ui.cbb_select_machine.clear()
                self.ui.cbb_select_machine.setHidden(False)
                if login[1] == MachineFunc.ReleaseMachine:
                    self.ui.cbb_select_machine.addItem(self.lang['machine']['release'])
                elif login[1] == MachineFunc.FormatMachine:
                    self.ui.cbb_select_machine.addItem(self.lang['machine']['format'])   
                elif login[1] == MachineFunc.MultiFuncMachine:
                    self.ui.cbb_select_machine.addItem(self.lang['machine']['release'])   
                    self.ui.cbb_select_machine.addItem(self.lang['machine']['format'])   

                infoUser = self.Library.GetInfo()
                if infoUser is not None:
                    print("infoUser: " + infoUser.ToString())
                    self.user_login.clear()
                    self.user_login.append(infoUser.id)
                    self.user_login.append(infoUser.name)
                    self.user_login.append(infoUser.email)
                    self.user_login.append(infoUser.sex)
                    self.user_login.append(infoUser.picture)

                    # Lấy tất cả thông số kỹ thuật của các lô tem trên Server
                    StampBatchPara = self.Library.GetStampBatchParameter()
                    if StampBatchPara is not None:
                        self.ui.cbb_setup_stamp.clear()
                        for item in StampBatchPara:
                            self.ui.cbb_setup_stamp.addItem(item.name)
                            print('StampBatchPara-----', item.__dict__)

                    self.status_machine = enum.sMachine.LOGIN_SUCCESS 
                else:
                    self.status_machine = enum.sMachine.LOGIN_FAILED
                
                self.ui.stackwget_main.setCurrentIndex(2)
                self.ui.stackwget_action.setCurrentIndex(0)

                self.ui.lbl_username.setText(self.lang['gui']['lbl_username'] + self.user_login[enum.iUser.NAME.value] + " ")
                self.ui.lbl_message_login.setText(self.lang['message_login']['INIT']) #INIT

            elif login == ResultLogin.NoAccess:
                self.ui.lbl_message_login.setText(self.lang['message_login']['NO_ACCESS']) 

            else:
                self.ui.lbl_message_login.setText(self.lang['message_login']['LOGIN_FAIL'])

        # except:
        #     self.ui.lbl_message_login.setText(self.lang['message_login']['ERROR_SERVER'])
        #     return False
    
    def slot_btn_logout(self):
        try:
            result = self.Library.Logout()
            self.ui.stackwget_main.setCurrentIndex(1)
        except:
            self.status_bar_mess = enum.sBar.ERROR_SERVER
            return False


    def slot_btn_logo_exit(self):
        self.close()
    

    def slot_btn_setup(self):
        gender = ['Nam', 'Nữ','Khác']
        url = self.user_login[enum.iUser.PICTURE.value]  
        image = QImage()
        image.loadFromData(requests.get(url).content)
        self.ui.lbl_setup_picture.setPixmap(QPixmap(image))
        self.ui.lbl_setup_name.setText(self.user_login[enum.iUser.NAME.value])
        self.ui.txt_setup_username.setText(self.user_login[enum.iUser.NAME.value])
        self.ui.txt_setup_email.setText(self.user_login[enum.iUser.EMAIL.value])
        if self.user_login[enum.iUser.SEX.value] is not None:
            self.ui.txt_setup_gender.setText(gender[int(self.user_login[enum.iUser.SEX.value])])

        self.ui.stackwget_main.setCurrentIndex(3)


    def slot_radioButton(self):
        if self.ui.radioButton.isChecked():
            self.variableRepository.Language = 'vi' # Lưu local giá trị ngôn ngữ
            self.ini_lang_sys('vi')
        elif self.ui.radioButton_2.isChecked():
            self.variableRepository.Language = 'en'
            self.ini_lang_sys('en')
        self.status_machine = enum.sMachine.SELECT_RO
        

    def stamp_batch_parameter_changed(self):
        out = self.ui.cbb_setup_stamp.currentText() # Giá trị đang chọn
        # Lấy tất cả thông số kỹ thuật của các lô tem trên Server
        StampBatchPara = self.Library.GetStampBatchParameter()
        if StampBatchPara is not None:
            for item in StampBatchPara:
                if item.name == out: # Chọn loại lô nào thì hiển thị thông tin của loại lô đó
                    self.ui.txt_setup_length_stamp.setText(str(item.length))
                    self.ui.txt_setup_width_stamp.setText(str(item.width))
                    self.ui.txt_setup_distance_stamp.setText(str(item.distance))
                    self.ui.txt_setup_id_stamp.setText(str(item.inner_diameter))
                    self.ui.txt_setup_od_stamp.setText(str(item.outer_diameter))
                    break

    
    # timer
    def slot_timeout_1s(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss')
        self.label_1.setText(timeDisplay)