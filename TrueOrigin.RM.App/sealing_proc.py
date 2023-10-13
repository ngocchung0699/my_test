import sys
import os
from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QDateTime
from PyQt5.QtGui import QMovie

from GPIO.DefineParameter import *
from Features.DTimer import DTimer
from Features.Worker import Worker
from Libraries.LibHandling import OrderType
from Process.FormattingMachine import FormattingMachine
from Process.ReleaseMachine import ReleaseMachine
import threading
sys.path.append("Database/Models")
from OrderReleaseModel import OrderReleaseModel

from Log.ConfigLog import ConfigLog
from Views.ViewHandling import ViewHandling

import enumerate.enum_init as enum

import time
import requests
import json

from PyQt5.QtCore import *

import Views.Ui.sealing_dialog as dialog
from GPIO.DefineParameter import ParaMachine

# GPIO & NFC532
system = ParaMachine.SYSTEM.value
if system == 'linux':
    from CardNFC.CardHandling import CardHandling
    from GPIO.Sensor import Sensor
    from GPIO.StepMortor import StepMotor
    from GPIO.Button import Button
    from GPIO.Buzzer import Buzzer
    from GPIO.DefinePin import *
                
class Sealing(ViewHandling):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_function()

    def user_function(self):
        self.ini_global()
        self.ini_qtimer()
        self.ini_connect_slot()
        self.ini_variable_system()
        self.InitLogger()

        lang = self.variableRepository.Language
        if lang is None: # Nếu csdl chưa chọn ngôn ngữ, thì chọn ngôn ngữ mặc định
            self.ini_lang_sys(ParaMachine.LANG_DEFAULT.value)
            self.variableRepository.Language = ParaMachine.LANG_DEFAULT.value
        else:
            self.ini_lang_sys(lang)

        self.InitMachine()

        if system == 'linux':
            self.initGPIO()

    def InitLogger(self):#Logger lưu sự kiện của máy
        cl = ConfigLog()
        # cl.StartRotateHandlers() #Tách log theo dung lượng file
        cl.StartTimeRotateHandlers() #Tách log theo thời gian
        ConfigLog.logger.info('STARTUP APP')

    def InitMachine(self):
        self.formatMachine = FormattingMachine(self.ui, self.lang)
        self.releaseMachine = ReleaseMachine(self.ui, self.lang)

    #     self.dlg = QtWidgets.QDialog()
    #     self.dlg.setWindowTitle("Loading")
    #     self.dlg.setWindowModality(False)
    #     self.dlg.setFixedSize(256, 256)
    #     self.dlg.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
    #     self.label_animation = QtWidgets.QLabel(self.dlg)
    #     self.movie = QMovie("Views/Ui/giphy1.gif")
    #     self.label_animation.setMovie(self.movie)
    #     self.show_loading = False
    #     t1 = threading.Thread(target=self.OnMovieLoading, args=())
    #     t1.start()

    # def start_animation(self):
    #     self.movie.start()
    #     self.dlg.show()

    # def stop_animation(self):
    #     self.movie.stop()
    #     self.dlg.done(0)
    # def OnMovieLoading(self):
    #     while True:
    #         if self.show_loading == True:
    #             time_old = time.time()
    #             while (time.time() - time_old < 4):
    #                 self.start_animation()
    #             self.stop_animation()
    #             self.show_loading = False

    def initGPIO(self):        #Init step motor
        self.motorRight = StepMotor(PinDirection= PinDirectionRight, PinEnable= PinEnableRight, PinStep= PinStepRight)
        self.motorRight.Disable()
        self.motorRight.DirCounterClockwise()
        self.motorRight.SetSpeed(ParaCalculation.MIN_SPEED_MOTOR)
        self.timerMotor = DTimer(1, self.ModulationSpeedMotor)
        self.StepTimesModulationSpeed = 0 #Số lần gọi didefu chế van toc
        self.StampSpeed = 0 #Van toc tuc thoi
        self.time_detect_old = 0

        self.motorLeft = StepMotor(PinDirection= PinDirectionLeft, PinEnable= PinEnableLeft, PinStep= PinStepLeft)
        self.motorLeft.Disable()

        #init sensor
        self.sensor = Sensor()
        self.sensor.DetectMetal.connect(self.ProcessSensorMetal)
        self.sensor_dectect = False
        self.allowDetectSensor = True

        #init button
        self.buttonLeft = Button(PinButton = PinButtonLeft, PinLed = PinLedLeft)
        self.buttonRight = Button(PinButton = PinButtonRight, PinLed = PinLedRight)

        self.buttonLeft.DetectButton.connect(self.ProcessButtonLeft)
        self.buttonRight.DetectButton.connect(self.ProcessButtonRight)

        self.TimerErrorNotification = DTimer(5, self.ErrorTem)
        self.allow_detect_tem_while_click_button = 0
        # self.timer_detect_tem.cancel()

        self.Buzzer = Buzzer(PinBuzzer= PinBuzzer)
        self.Buzzer.Disable()
        
        self.cnt_tem_error = 0 
        self.cnt_tem = 0 

        # self.temfinish = DTimer(0.5, self.detect_tem_finish, [4])
        self.allow_detect_tem_while_run = 0
        self.time_detect_old_on_run = 0

        self.releasing_state_busy = False
        
        print("find the first stamp")
        self.first_tem = False
        if(self.first_tem == False):
            self.motorRight.SetSpeed(10)
            self.motorRight.Enable()
            self.motorRight.DirCounterClockwise()
            self.motorRight.Run()
            self.allowDetectSensor = True
        self.first_tem_come_back=False
        time.sleep(0.3)
        while(self.first_tem_come_back==False):
            if self.first_tem == True:
                self.motorRight.Disable()
                time.sleep(0.3)
                self.motorLeft.SetSpeed(5)
                self.motorLeft.Enable()
                self.motorLeft.DirClockwise()
                self.motorLeft.Run()
                time.sleep(0.5)
                self.motorLeft.Disable()
                self.first_tem_come_back==True
                self.first_tem = False
                break
    

    def detect_tem_finish(self, waiting_time = 4):
        # print("nhan dang tem cuoi cung ------------------")
        if self.allow_detect_tem_while_run == 1:
            # print("time ---------: ", time.time() - self.time_detect_old_on_run)
            if (time.time() - self.time_detect_old_on_run) >= waiting_time:
                
                self.motorRight.Disable()
                self.motorLeft.Disable()

                # print("dung chay --------------")
                self.button_setEnable(self.ui.btn_start, True, self.lang['status_bt']['CONTINUE'])
                self.status_releasing = enum.sReleasing.IDLE
                self.status_machine = enum.sMachine.PAUSE

                self.allow_detect_tem_while_run = 0
                
                self.temfinish.cancel()
                self.TimerErrorNotification = DTimer(5, self.ErrorTem)
                self.TimerErrorNotification.start()

    def ErrorTem(self):
        for i in range(0, 4):
            if ((i%2) == 0):
                self.Buzzer.Enable()
                # print("on")
            if ((i%2) == 1):
                # print("off")
                self.Buzzer.Disable()
            if i >= 3:
                # print("out")
                self.Buzzer.Disable()
                # self.TimerErrorNotification.cancel()
            time.sleep(0.5)
        self.TimerErrorNotification.cancel()
    def ProcessButtonLeft(self):  # nút bấm bên trái - động cơ bên trái cuộn tem
        if self.buttonRight.Busy() == False:
            if self.buttonLeft.ClickButton()== 1:
                self.buttonLeft.LedButton(1)
                self.allowDetectSensor = False
                self.allow_detect_tem_while_click_button = 0
                self.time_detect_old = time.time()
                self.timer_detect_tem = DTimer(0.1, self.detect_tem)
                self.timer_detect_tem.start()
                self.buttonLeft.SetClickButton(2)
                self.buttonRight.allowCheck(False)
                self.motorRight.Disable()
                self.motorLeft.SetSpeed(40)
                self.motorLeft.Enable()
                self.motorLeft.DirClockwise()
                self.motorLeft.Run()
            if self.buttonLeft.ClickButton()== 0:
                self.buttonLeft.LedButton(0)
                self.timer_detect_tem.cancel()
                self.allowDetectSensor = True
                self.buttonRight.allowCheck(True)
                self.motorLeft.Disable()

    def ProcessButtonRight(self):        # nút bấm bên phải - động cơ bên phải cuộn tem
        if self.buttonLeft.Busy() == False:
            if self.buttonRight.ClickButton() == 1:
                self.buttonRight.LedButton(1)
                self.allowDetectSensor = False
                self.allow_detect_tem_while_click_button = 0
                self.time_detect_old = time.time()
                self.timer_detect_tem = DTimer(0.1, self.detect_tem)
                self.timer_detect_tem.start()
                self.buttonRight.SetClickButton(2)
                self.buttonLeft.allowCheck(False)
                self.motorLeft.Disable()
                self.motorRight.SetSpeed(40)
                self.motorRight.Enable()
                self.motorRight.DirCounterClockwise()
                self.motorRight.Run()
            if self.buttonRight.ClickButton() == 0:
                self.buttonRight.LedButton(0)
                self.timer_detect_tem.cancel()
                self.allowDetectSensor = True
                self.buttonLeft.allowCheck(True)
                self.motorRight.Disable()
    def detect_tem(self):            # nhận biết có tem khi chạy ở chế độ nút bấm
        if self.allow_detect_tem_while_click_button == 1:
            if (time.time() - self.time_detect_old) >= 0.7:
                self.motorRight.Disable()
                self.motorLeft.Disable()
                self.buttonRight.SetClickButton(0)
                # self.buttonLeft.SetClickButton(0)
                self.ProcessButtonRight()
                self.ProcessButtonLeft()
                if self.buttonLeft.ClickButton() == 2:
                    self.buttonLeft.SetClickButton(0)
                    self.first_tem = False
                    while(self.first_tem == False):

                        self.motorLeft.SetSpeed(5)
                        time.sleep(0.2)
                        self.motorLeft.Stop()
                        self.motorLeft.Disable()
                        self.motorRight.SetSpeed(10)
                        self.motorRight.Enable()
                        self.motorRight.DirCounterClockwise()
                        self.motorRight.Run()
                        
                    time.sleep(0.5)
                    self.motorRight.Disable()
                    self.motorLeft.SetSpeed(10)
                    self.motorLeft.Enable()
                    self.motorLeft.DirClockwise()
                    self.motorLeft.Run()
                    time.sleep(0.5)
                    self.motorLeft.Disable()
                    self.motorRight.Disable()
                    print("The button is turned off, the motor stop")
                
    def ProcessSensorMetal(self): # Phát hiện tem
        self.first_tem = True
        if self.allowDetectSensor == True: 
            self.cnt_tem +=1
            # ConfigLog.logger.info('da dem duoc %s tem', self.cnt_tem)
            #Dừng motor để đọc tem
            self.StopMotor()
            if self.status_releasing == enum.sReleasing.NEXT_STAMP:
                self.status_releasing = enum.sReleasing.INIT
            
            self.CalculateSpeed() # Khi phát hiện tem, thì tính toán vận tốc chạy động cơ cho lần tiếp theo
            self.sensor_dectect = True
            self.motorRight.SetSpeed(15)
            # self.SetSpeedMotor(20)
            # print('Detect stamp')
        if self.allowDetectSensor == False:
            self.time_detect_old = time.time()
            self.allow_detect_tem_while_click_button = 1

    def ini_global(self):
        global COUNT_NEXT_STAMP
        global NUM_SEAL_TRY
        global COUNT_BAR_TO
        global URL_SERVER

    def ini_qtimer(self):
        self.timer_clock    = QTimer()
        self.timer_machine  = QTimer()
        self.time_status_bar = QTimer()

    def ini_connect_slot(self):
        self.timer_clock.timeout.connect(self.slot_timeout_1s)
        self.timer_machine.timeout.connect(self.slot_machine_state)
        self.time_status_bar.timeout.connect(self.slot_statusBar_state)

        self.ui.btn_login.clicked.connect(self.slot_btn_login) # Nút đăng nhập
        self.ui.btn_logout.clicked.connect(self.slot_btn_logout) # Nút đăng xuất
        self.ui.btn_start.clicked.connect(self.slot_btn_start) #Nút bắt đầu chạy máy phát hành
        # self.ui.btn_emergency.clicked.connect(self.slot_btn_emergency) #Nút dừng khẩn cấp
        self.ui.btn_return.clicked.connect(self.slot_btn_return) #Nút quay lại

        self.ui.btn_select.clicked.connect(self.slot_btn_select) #Nút chọn lệnh phát hành
        self.ui.btn_format_select.clicked.connect(self.slot_btn_select) #Nút chọn lệnh format

        self.ui.btn_refresh_orders.clicked.connect(self.slot_btn_refresh_orders) #Nút làm mới danh sách lệnh phát hành
        self.ui.btn_refresh_format_orders.clicked.connect(self.slot_btn_refresh_orders) #Nút làm mới danh sách lệnh format

        self.ui.btn_close.clicked.connect(self.slot_btn_close)
        self.ui.btn_detail_success.clicked.connect(self.slot_btn_detail_success)
        self.ui.btn_setup.clicked.connect(self.slot_btn_setup)
        self.ui.btn_return_setup.clicked.connect(self.slot_btn_return_setup)
        self.ui.btn_sealing_manual.clicked.connect(self.slot_btn_sealing_manual)
        # self.ui.btn_sync_ro_manual.clicked.connect(self.slot_btn_sync_ro_manual)
        self.ui.btn_repair_ro.clicked.connect(self.slot_btn_repair_ro)

        self.ui.table_list_istamp.itemClicked.connect(self.slot_get_info_id)
        self.ui.table_releaser_order.itemClicked.connect(self.slot_table_releaser_order) # Event click 1 item trong bảng danh sách lệnh phát hành lấy từ server

        # setup
        self.ui.btn_setup_info.clicked.connect(self.slot_btn_setup_info) # Nút hiển thị thông tin cá nhân
        self.ui.btn_setup_lang.clicked.connect(self.slot_btn_setup_lang) # Nút cài đặt ngôn ngữ
        self.ui.btn_setup_stamp.clicked.connect(self.btn_setup_stamp) # Nút cài đặt thông số của tem
        self.ui.btn_setup_return.clicked.connect(self.slot_btn_return_setup) # Nút quay lại của màn cài đặt

        self.ui.radioButton.toggled.connect(self.slot_radioButton) # Radio Chọn ngôn ngữ

        self.ui.cbb_setup_stamp.currentTextChanged.connect(self.stamp_batch_parameter_changed) #chọn loại lô tem
        self.ui.cbb_select_machine.currentTextChanged.connect(self.select_machine, ) #chọn loại máy( phát hành, format, ...)

    def close_slot(self):
        self.timer_clock.stop()
        self.timer_machine.stop()
        self.time_status_bar.stop()
        self.timerMotor.cancel()
        self.sensor.StopReadSensor()

    #event double click UI
    def mouseDoubleClickEvent( self, event ):
        if event.button() == Qt.LeftButton:
            widget = self.childAt(event.pos())
            if widget is not None and widget.objectName():
                if widget.objectName() == 'btn_logo_exit': #nếu db click logo ở thi thot
                    result = QtWidgets.QMessageBox.question(
                        self, 'Confirm Close', 'Are you sure you want to close the app?',
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    if result == QtWidgets.QMessageBox.Yes:
                        self.close_slot()
                        self.slot_btn_logo_exit()
                        ConfigLog.logger.info('CLOSE APP')
                        event.accept()
                        self.Buzzer.Disable()
                        os.system("killall python3")
                    else:
                        event.ignore()
        return

    def ini_variable_system(self):
        self.Error              = "UnknownError" # Mã lỗi sinh ra trong quá trình release/format
        self.numtry_seal        = None # Số lần thử phát hành lại 1 tem
        self.selected_ro        = None
        self.detect_stamp       = None
        self.id_batch_cur       = None
        self.token_current      = None
        self.seri_number_cur    = None
        self.count_next_stamp   = None
        self.number_display     = {"start_seri":0, "num_success": 0, "num_fail": 0, "num_seri_cur": 0, "number_cur": 0}
        self.statusRO           = []
        self.list_ro            = []
        self.user_login         = []
        self.block_number       = 6
        self.status_releasing   = enum.sReleasing.INIT
        self.OrderType          = OrderType.NoneType

        self.ui.btn_repair_ro.setVisible(False)
        self.label_1 = QtWidgets.QLabel("")
        self.label_1.setObjectName("lbl_clock")
        self.label_1.setStyleSheet("#lbl_clock { color:#464646;}")
        # self.label_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ui.statusBar.addPermanentWidget(self.label_1)
        self.ui.statusBar.setObjectName("statusBar")
        self.ui.statusBar.setStyleSheet("#statusBar { outline: none; }")

        self.timer_clock.start(1000)
        self.timer_machine.start(500)
        self.time_status_bar.start(200)

        self.status_bar_mess    = enum.sBar.IDLE
        self.status_machine     = enum.sMachine.LOGIN

        self.flag_stop_thread   = {"approving_login": False, "approving_change_ro": False, "process_releasing": False }
        self.threadpool         = QThreadPool()
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Sealing - ID " + str(self.variableRepository.MachineId)))

        self.FlagPause = False # cờ tạm dừng 

    def StartMotor(self):
        self.allowDetectSensor = False
        self.motorLeft.Disable()
        self.motorRight.SetSpeed(15)
        self.motorRight.Enable()
        self.motorRight.DirCounterClockwise()
        self.motorRight.Run()
        time.sleep(0.2)
        self.allowDetectSensor = True
        self.SetSpeedMotor()
        ParaCalculation.TDetectStamp = time.time() #gán thời điểm bắt đầu chạy motor

    def StopMotor(self):
        self.allow_detect_tem_while_run = 0
        self.motorRight.Disable() # Dừng motor
        self.timerMotor.cancel() # dừng quá trình tính toán tốc độ động cơ trong 1 chu kỳ chạy
        # ConfigLog.logger.critical('Motor Run Time %s', time.time()-ParaCalculation.TDetectStamp) #thời điểm dừng motor

    def SetSpeedMotor(self):
        self.StepTimesModulationSpeed = 0
        # print("SetSpeedMotor")
        # print(str(ParaCalculation.DeltaTime))
        if ParaCalculation.DeltaTime != 0:
            
            delay = ParaCalculation.DeltaTime/10 # Chia khoảng thời gian phát hiện tem làm 10 đoạn. tương ứng mỗi đoạn sẽ set vận tốc hợp lý
            
            self.timerMotor = DTimer(delay, self.ModulationSpeedMotor)
            self.timerMotor.start()

    #Tính toán speed motor, trong 1 lần chạy tem - vận tốc motor sẽ dạng hình thang vuông, giúp quá trình dừng mượt hơn (giảm 10% vận tốc mỗi khoảng)
    def ModulationSpeedMotor(self): #Thời gian giảm đần đều vn tốc motor
        
        if self.StepTimesModulationSpeed < 1:
            self.StampSpeed = ParaCalculation.MIN_SPEED_MOTOR
        else:
            self.StampSpeed = ParaCalculation.MAX_SPEED_MOTOR - ParaCalculation.MAX_SPEED_MOTOR*self.StepTimesModulationSpeed*0.1

        if self.StampSpeed < ParaCalculation.MIN_SPEED_MOTOR:
            self.StampSpeed = ParaCalculation.MIN_SPEED_MOTOR
        
        self.motorRight.SetSpeed(self.StampSpeed)
        self.StepTimesModulationSpeed += 1
        # print("StepTimesModulationSpeed ", self.StepTimesModulationSpeed)
        # print("StampSpeed", self.StampSpeed)
        # ConfigLog.logger.critical('Speed Motor %s', self.StampSpeed)
        
    #Tính toán speed motor, thay đổi qua mỗi lần chạy tem
    def CalculateSpeed(self):
        if ParaCalculation.TDetectStamp != 0:
            ParaCalculation.DeltaTime = time.time() - ParaCalculation.TDetectStamp #Khoảng thời gian giữa 2 lần phát hiện tem

    # Máy trạng thái
    def slot_machine_state(self):
        # Hệ thống
        if(self.status_machine == enum.sMachine.IDLE):
            return
        elif(self.status_machine == enum.sMachine.LOGIN):
            self.button_setEnable(self.ui.btn_select, False)
            self.button_setEnable(self.ui.btn_format_select, False)
            self.button_setEnable(self.ui.btn_refresh_orders, False)
            self.button_setEnable(self.ui.btn_return, False)
            
            self.ui.stackwget_main.setCurrentIndex(1)
            self.status_machine = enum.sMachine.IDLE
            return

        elif(self.status_machine == enum.sMachine.LOGIN_SUCCESS):
            self.get_order()
            self.button_setEnable(self.ui.btn_select, False)
            self.button_setEnable(self.ui.btn_format_select, False)
            self.status_bar_mess = enum.sBar.INIT
            self.status_machine = enum.sMachine.IDLE
            return
        elif self.status_machine == enum.sMachine.APPROVING:
            self.ui.lbl_message_login.setText(self.lang['message_login']['LOGIN_SUCCESS'])

            worker = Worker(self.run_check_approving_login)
            self.threadpool.start(worker)

            self.button_setEnable(self.ui.btn_login, False)
            self.status_machine = enum.sMachine.IDLE
            return
        elif self.status_machine == enum.sMachine.UPDATE_RO:
            self.get_order()
            self.status_machine = enum.sMachine.IDLE
            return
        elif(self.status_machine == enum.sMachine.SELECT_RO):
            self.get_order()

            self.button_setEnable(self.ui.btn_select, False)
            self.button_setEnable(self.ui.btn_format_select, False)
            self.status_bar_mess = enum.sBar.INIT
            self.status_machine = enum.sMachine.IDLE
            return
        elif self.status_machine == enum.sMachine.CHANGE_RO:
            # worker = Worker(self.run_check_approving_ro)
            # self.threadpool.start(worker)

            self.get_order()
            self.status_machine = enum.sMachine.IDLE
            return
        elif(self.status_machine == enum.sMachine.READY):
            self.button_setEnable(self.ui.btn_start, True, self.lang['status_bt']['START'])
            # self.button_setEnable(self.ui.btn_return, True)
            self.status_bar_mess = enum.sBar.READY
            self.ui.stackwget_action.setCurrentIndex(2)
            self.status_machine = enum.sMachine.IDLE
            return
        elif(self.status_machine == enum.sMachine.RELEASING):
            # self.status_machine = enum.sMachine.IDLE
            return
        elif(self.status_machine == enum.sMachine.PAUSE):
            
            self.button_setEnable(self.ui.btn_start, True, self.lang['status_bt']['CONTINUE'])
            # self.button_setEnable(self.ui.btn_return, True)
            self.status_bar_mess = enum.sBar.PAUSE
            # self.ui.stackwget_action.setCurrentIndex(1)
            # self.status_machine = enum.sMachine.IDLE
            return
        elif(self.status_machine == enum.sMachine.STOP):
            return
        elif self.status_machine == enum.sMachine.COMPLETE:

            return
        
    #Máy trạng thái trong quá trình phát hành tem
    def slot_releasing_state(self, progress_callback):
        self.flag_stop_thread['process_releasing'] = True
        
        self.stampStt = None
        self.machineStt = None
        self.to = time.time()
        self.releasing_state_busy = True
        allow_cnt_error = False
        while(self.flag_stop_thread['process_releasing']): 
            if self.stampStt != self.status_releasing:
                ConfigLog.logger.info('Stt--- %s -- %s', self.status_releasing, time.time()-self.to)
                self.to = time.time()
                self.stampStt = self.status_releasing

            if self.machineStt != self.status_machine:
                ConfigLog.logger.info('Stt Machine--- %s -- %s', self.status_machine, time.time()-self.to)
                self.machineStt = self.status_machine

            if(self.status_releasing == enum.sReleasing.INIT):
                self.numtry_seal = 0
                self.count_next_stamp = 0
                self.detect_stamp = False
                progress_callback.emit(enum.sReleasing.INIT.value)
                self.status_releasing = enum.sReleasing.DETECT_STAMP
                
            elif(self.status_releasing == enum.sReleasing.DETECT_STAMP): # trạng thái cảm biến phát hiện tem
                if int(self.count_next_stamp) < ParaMachine.COUNT_NEXT_STAMP.value:
                    self.count_next_stamp = self.count_next_stamp + 1
                    # if self.sensor_dectect == True:
                    #     self.sensor_dectect = False

                    if self.ui.cbb_select_machine.currentText() == self.lang['machine']['release']:
                        self.number_display["num_seri_cur"] = self.number_display["start_seri"] + self.number_display["num_success"] 

                    self.status_releasing = enum.sReleasing.PAUSE_PUSH
                    progress_callback.emit(enum.sReleasing.PAUSE_PUSH.value)

                else:
                    self.status_releasing = enum.sReleasing.ALARM_STOPSS
                    progress_callback.emit(enum.sReleasing.ALARM_STOPSS.value)

            elif(self.status_releasing == enum.sReleasing.PAUSE_PUSH): # stt dừng động cơ để bắt đầu tiến hành release, format
                if(self.OrderType == OrderType.Release): #Nếu là lệnh phát hành
                    allow_cnt_error = True
                    resultRelease, numberRelease = self.Library.ReleaseStamp(self.selected_ro)
                    if resultRelease is True: # phát hành thành công
                        self.number_display["num_success"] = numberRelease
                        self.number_display["number_cur"] = self.number_display["num_success"]
                        self.status_releasing = enum.sReleasing.UPDATE # Báo cập nhật UI
                        
                    elif resultRelease is None: # lô hoàn thành, báo hoàn thành
                        self.number_display["num_success"] = numberRelease
                        self.number_display["number_cur"] = self.number_display["num_success"]
                        progress_callback.emit(enum.sReleasing.UPDATE.value)
                        self.status_releasing = enum.sReleasing.COMPLETE
                        self.buttonLeft.SetClickButton(1)
                        self.buttonLeft.DetectButton.emit()

                    else: # ko phát hành được tem, thì lưu số thứ tự tem phát hành lỗi, và thử lại
                        # self.Library.UpdateSeriReleased(order_id = self.selected_ro.order_id, no_number= release.no_number, IsReleased= False) # Cập nhật cho Local biết số seri này phát hành chưa thành công
                        self.status_releasing = enum.sReleasing.TRY_COUNT
                        self.Error = resultRelease # Hiển thị mã lỗi
                        ConfigLog.logger.critical('Release Err--- %s', resultRelease)
                    # self.button_setEnable(self.ui.btn_return, True)
                elif(self.OrderType == OrderType.Format): #Nếu là lệnh xuất xưởng
                    allow_cnt_error = True
                    resultFormat, numberFormat = self.Library.FormatStamp(self.selected_ro)
                    if resultFormat is True: # format thành công
                        self.number_display["num_success"] = numberFormat
                        self.number_display["number_cur"] = self.number_display["num_success"]
                        self.status_releasing = enum.sReleasing.UPDATE # Báo cập nhật UI
                        
                    elif resultFormat is None: # lô hoàn thành, báo hoàn thành
                        self.number_display["num_success"] = numberFormat
                        self.number_display["number_cur"] = self.number_display["num_success"]
                        progress_callback.emit(enum.sReleasing.UPDATE.value)
                        self.status_releasing = enum.sReleasing.COMPLETE
                        self.buttonLeft.SetClickButton(1)
                        self.buttonLeft.DetectButton.emit()


                    else: # ko format được tem
                        self.status_releasing = enum.sReleasing.TRY_COUNT
                        self.Error = resultFormat # Hiển thị mã lỗi
                        ConfigLog.logger.critical('Format Err--- %s', resultFormat)

                    # self.button_setEnable(self.ui.btn_return, True)
            elif(self.status_releasing == enum.sReleasing.UPDATE): # stt Update
                progress_callback.emit(enum.sReleasing.UPDATE.value)

                self.status_releasing = enum.sReleasing.NEXT_STAMP
                progress_callback.emit(enum.sReleasing.NEXT_STAMP.value)
                
            elif(self.status_releasing == enum.sReleasing.TRY_COUNT):
                progress_callback.emit(enum.sReleasing.TRY_COUNT.value)
                if int(self.numtry_seal) < ParaMachine.NUM_SEAL_TRY.value:
                    self.numtry_seal = self.numtry_seal + 1
                    self.status_releasing = enum.sReleasing.PAUSE_PUSH
                else:
                    self.status_releasing = enum.sReleasing.ALARM_STOPSS
                    progress_callback.emit(enum.sReleasing.ALARM_STOPSS.value)

            elif(self.status_releasing == enum.sReleasing.ALARM_STOPSS):
                if allow_cnt_error == True:
                    self.cnt_tem_error += 1
                    data = "so tem bi loi " + str(self.cnt_tem_error)
                    print(data)
                    self.ui.lbl_num_fail.setText(str(self.cnt_tem_error))
                    ConfigLog.logger.info('Error stamps. number Error: %s', self.cnt_tem_error)
                    self.flag_stop_thread['process_releasing'] = False
                    # self.button_setEnable(self.ui.btn_emergency, True, self.lang['status_bt']['RUN'])
                    self.button_setEnable(self.ui.btn_start, True, self.lang['status_bt']['CONTINUE'])
                    self.status_releasing = enum.sReleasing.IDLE
                    self.status_machine = enum.sMachine.PAUSE

                    # self.button_setEnable(self.ui.btn_return, True)

            elif self.status_releasing == enum.sReleasing.NEXT_STAMP:
                #Next tem sẽ không làm gì, chờ đợi động cơ chạy - Vì trạng thái này sẽ liên tục được thực thi từ lúc động cơ chạy -> dừng
                if self.FlagPause:
                    self.flag_stop_thread['process_releasing'] = False

            elif self.status_releasing == enum.sReleasing.COMPLETE:
                progress_callback.emit(enum.sReleasing.COMPLETE.value)
                self.status_bar_mess = enum.sBar.COMPLETE
                self.status_releasing = enum.sReleasing.IDLE

            elif(self.status_releasing == enum.sReleasing.STOP):
                print(self.status_releasing)

        self.releasing_state_busy = False
        self.button_setEnable(self.ui.btn_return, True)

    def progress_fn(self, st_releasing):
        if self.ui.cbb_select_machine.currentText() == self.lang['machine']['format']:
            self.ui.label_17.clear()
        if(st_releasing == enum.sReleasing.INIT.value):
            self.ui.rtb_progress_release.clear()
            pass
        
        elif st_releasing == enum.sReleasing.PAUSE_PUSH.value:
            if self.ui.cbb_select_machine.currentText() != self.lang['machine']['format']:
                self.ui.lbl_numberSeri.setText(str(self.number_display["num_seri_cur"]))
            self.ui.rtb_progress_release.appendPlainText(self.lang['progress_fn'][ 'INIT'])
            self.ui.rtb_progress_release.appendPlainText(self.lang['progress_fn']['PAUSE_PUSH'])

        elif(st_releasing == enum.sReleasing.TRY_COUNT.value):
            self.ui.rtb_progress_release.appendPlainText(self.lang['progress_fn']['TRY_COUNT'] + " CE: " + self.Error)

        elif(st_releasing == enum.sReleasing.ALARM_STOPSS.value):
            self.ui.rtb_progress_release.appendPlainText(self.lang['progress_fn']['ALARM_STOPSS'])
            self.button_setEnable(self.ui.btn_start, True, self.lang['status_bt']['START'])
            self.status_machine = enum.sMachine.PAUSE
            self.status_releasing = enum.sReleasing.ALARM_STOPSS
            self.status_bar_mess = enum.sBar.PAUSE
            self.TimerErrorNotification = DTimer(5, self.ErrorTem)
            self.TimerErrorNotification.start()

        elif(st_releasing == enum.sReleasing.UPDATE.value):
            timer = QDateTime.currentDateTime()
            timeDisplay = timer.toString('yyyy-MM-dd hh:mm:ss')
            # stamp = (self.number_display["number_cur"], self.ui.lbl_numberSeri.text(), timeDisplay, 'success', self.selected_ro.order_id)

            # with self.conn:
            #     new_stamp = self.db.insert_stamp(self.conn, stamp)
            # if(new_stamp):
            #     row = self.ui.table_list_istamp.rowCount()
            #     self.ui.table_list_istamp.setRowCount(row + 1)
            #     self.ui.table_list_istamp.setItem(row, 0, QtWidgets.QTableWidgetItem(str(new_stamp)))
            #     self.ui.table_list_istamp.setItem(row, 1, QtWidgets.QTableWidgetItem(str(stamp[0])))
            #     self.ui.table_list_istamp.setItem(row, 2, QtWidgets.QTableWidgetItem(str(stamp[1])))
            #     self.ui.table_list_istamp.setItem(row, 3, QtWidgets.QTableWidgetItem(str(stamp[2])))
            #     self.ui.table_list_istamp.setItem(row, 4, QtWidgets.QTableWidgetItem(str(stamp[4])))
            if self.ui.cbb_select_machine.currentText() != self.lang['machine']['format']:
                self.ui.rtb_progress_release.appendPlainText(self.lang['progress_fn']['SUCCESSFUL'] + " seri: " + str(self.number_display["num_seri_cur"]))
            else:
                self.ui.rtb_progress_release.appendPlainText(self.lang['progress_fn']['SUCCESSFUL'] )

            number_comlete = self.number_display["number_cur"]
            self.ui.lbl_num_success.setText(str(self.number_display["num_success"]))
            try: 
                self.func_set_progress(number_comlete, self.selected_ro.total_seri)
            except:
                self.func_set_progress(number_comlete, self.selected_ro.total_number)

           

        elif st_releasing == enum.sReleasing.NEXT_STAMP.value:
            # print("dong co chay o day--------------")
            if self.FlagPause == False:
                self.StartMotor()
                self.time_detect_old_on_run = time.time()
                self.allow_detect_tem_while_run = 1
                
        elif st_releasing == enum.sReleasing.COMPLETE.value:
            # self.button_setEnable(self.ui.btn_emergency, False, self.lang['status_bt']['RUN'] )
            self.button_setEnable(self.ui.btn_start, False, self.lang['status_bt']['PAUSE'])
            # self.button_setEnable(self.ui.btn_return, True)
            self.button_setEnable(self.ui.btn_logout, True)
            # self.button_setEnable("btn_compelte", False, self.lang['status_bt']['PAUSE'])

            id_ro = self.selected_ro.order_id
            current_seri = self.number_display["number_cur"] + 1
            # self.db.update_ro_local(self.conn, id_ro, current_seri, enum.sRO.COMPLETE.value)
            self.flag_stop_thread['process_releasing'] = False
            self.status_machine == enum.sMachine.COMPLETE

        elif st_releasing == enum.sReleasing.STOP.value:
            print(st_releasing)

    def slot_statusBar_state(self):
        # status bar
        if self.status_bar_mess == enum.sBar.INIT:
            self.button_setStatus("INIT", self.lang['statusBar']['INIT'])
            self.status_bar_mess = enum.sBar.IDLE
        elif self.status_bar_mess == enum.sBar.ACTION:
            self.button_setStatus("RELEASING", self.lang['statusBar']['ACTION'])
            self.status_bar_mess = enum.sBar.IDLE
        elif self.status_bar_mess == enum.sBar.UPDATE:
            self.button_setStatus("RELEASING", self.lang['statusBar']['UPDATE'])
            self.count_status_bar_return = ParaMachine.COUNT_BAR_TO.value
            self.status_bar_mess = enum.sBar.COUNT_TIME
        elif self.status_bar_mess == enum.sBar.EXPORT:
            self.button_setStatus("RELEASING", self.lang['statusBar']['EXPORT'])
            self.count_status_bar_return = ParaMachine.COUNT_BAR_TO.value
            self.status_bar_mess = enum.sBar.COUNT_TIME
        elif self.status_bar_mess == enum.sBar.CHANGE_RO:
            self.button_setStatus("RELEASING", self.lang['statusBar']['CHANGE_RO'])
            self.status_bar_mess = enum.sBar.IDLE
        elif self.status_bar_mess == enum.sBar.ERROR_SERVER:
            self.button_setStatus("STOP", self.lang['statusBar']['ERROR_SERVER'])
        elif self.status_bar_mess == enum.sBar.ERROR_NFC:
            self.button_setStatus("STOP", self.lang['statusBar']['ERROR_NFC'])
        elif self.status_bar_mess == enum.sBar.COUNT_TIME:
            if(self.count_status_bar_return > 0):
                self.count_status_bar_return = self.count_status_bar_return - 1
                if self.count_status_bar_return == 0:
                    self.status_bar_mess = enum.sBar.ACTION
        elif self.status_bar_mess == enum.sBar.PAUSE:
            self.button_setStatus("PAUSE", self.lang['statusBar']['PAUSE'])
            self.status_bar_mess = enum.sBar.IDLE
        elif self.status_bar_mess == enum.sBar.READY:
            self.button_setStatus("READY", self.lang['statusBar']['READY'])
            self.status_bar_mess = enum.sBar.IDLE
        elif self.status_bar_mess == enum.sBar.COMPLETE:
            self.button_setStatus("COMPLETE", self.lang['statusBar']['COMPLETE_MESS'])
            QtWidgets.QMessageBox.about(self, self.lang['statusBar']['COMPLETE'], self.lang['statusBar']['COMPLETE_MESS'])
            self.status_bar_mess = enum.sBar.IDLE
            

    #------------------------------------------------------- CÁC SỰ KIỆN NÚT NHẤN -------------------------------------------------------#
    # Nút bắt đầu/Tạm dừng
    def slot_btn_start(self):
        if self.status_machine != enum.sMachine.RELEASING:
            print('button Start----------------------')
            
            # tắt thông báo tem lỗi
            self.TimerErrorNotification.cancel()
            # Bắt đầu
            self.button_setEnable(self.ui.btn_start, True, self.lang['status_bt']['PAUSE'])
            self.button_setEnable(self.ui.btn_return, False)

            # Chuyển trạng thái
            self.status_releasing = enum.sReleasing.INIT
            worker = Worker(self.slot_releasing_state)
            worker.signals.progress.connect(self.progress_fn)
            self.threadpool.start(worker)

            self.status_machine = enum.sMachine.RELEASING
            self.status_bar_mess = enum.sBar.ACTION

            self.FlagPause = False

            #Chạy động cơ
            # print("start ----------------------------------------")
            self.StartMotor()

            time_fin = 1.5 # ở trạng thái phát hành thì sau 1.5s k phát hiện tem thì báo hết tem
            self.temfinish = DTimer(0.2, self.detect_tem_finish, args=[time_fin])
            self.temfinish.start()
            # self.time_detect_old_on_run = time.time()
            
        elif self.status_machine == enum.sMachine.RELEASING:
            print("tam dung")
            self.temfinish.cancel()
            # Tạm dừng
            self.button_setEnable(self.ui.btn_start, True, self.lang['status_bt']['START'])
            # self.button_setEnable(self.ui.btn_return, True)
            # self.button_setEnable(self.ui.btn_emergency, False, self.lang['status_bt']['RUN'])

            # self.flag_stop_thread['process_releasing'] = False
            self.FlagPause = True
            self.status_machine = enum.sMachine.PAUSE
            self.status_releasing = enum.sReleasing.ALARM_STOPSS
            self.status_bar_mess = enum.sBar.PAUSE

            #Dừng động cơ
            self.StopMotor()

    # Nút dừng khẩn cấp
    def slot_btn_emergency(self):
        self.status_releasing = enum.sReleasing.INIT
        self.button_setEnable(self.ui.btn_emergency, False, self.lang['status_bt']['RUN'])
        # self.timer_clock.stop()
        # self.timer_machine.stop()

    # Nút quay lại
    def slot_btn_return(self):
        self.ui.cbb_select_machine.setHidden(False)
        self.TimerErrorNotification.cancel()
        self.Library.UnSelectOder(self.selected_ro.order_id, self.OrderType) #bỏ chọn Order đang chọn
        self.get_order() # lấy lại list order từ server
        self.button_setEnable(self.ui.btn_select, False)
        self.button_setEnable(self.ui.btn_format_select, False)
        self.button_setEnable(self.ui.btn_repair_ro, False)

        self.selected_ro = None #Clear biến lưu ro đang chọn

        # self.ui.stackwget_action.setCurrentIndex(0)
    
    def slot_btn_sealing_manual(self):
        print("enter sealing manual")

    def slot_btn_repair_ro(self):
        self.ui.btn_setup.setEnabled(False)
        id = self.ui.label.text().split(": ")[1]

        for item in self.list_ro:
            if str(item.order_id) == str(id):
                current_ro = str(item.no_number)
                start_ro = "0" #str(item.start_seri)
                end_ro = str(item.total_seri)

        # r = self.ui.table_releaser_order.currentRow()
        # id = self.ui.table_releaser_order.item(r,0).text()
        # current_ro = self.ui.table_releaser_order.item(r,3).text()
        # start_ro = self.ui.table_releaser_order.item(r,2).text()
        # end_ro = str(int(self.ui.table_releaser_order.item(r,1).text()) + int(self.ui.table_releaser_order.item(r,2).text()))

        self.dialog_ro = dialog.RepairRo()
        self.dialog_ro.id_ro = id
        self.dialog_ro.start_ro = start_ro
        self.dialog_ro.end_ro = end_ro
        self.dialog_ro.current_ro = current_ro
        self.dialog_ro.lang = self.lang['dialog']

        self.dialog_ro.draw()
        self.dialog_ro.show()
        if self.dialog_ro.exec():
            # self.db.update_ro_local(self.conn, id, self.dialog_ro.current_ro)
            self.button_setEnable(self.ui.btn_repair_ro, False)
            self.button_setEnable(self.ui.btn_select, False)
            self.button_setEnable(self.ui.btn_format_select, False)
            self.get_order()

        self.ui.btn_setup.setEnabled(True)
    
    def slot_btn_return_setup(self):
        self.ui.stackwget_main.setCurrentIndex(2)
    
    def slot_btn_select(self):
        # Lựa chọn lệnh phát hành
        self.ui.cbb_select_machine.setHidden(True)
        if self.ui.cbb_select_machine.currentText() == self.lang['machine']['format']:
            self.ui.label_17.clear()
        else:
            _translate = QtCore.QCoreApplication.translate
            self.ui.label_17.setText(_translate("MainWindow", "Số seri đang phát hành:"))
        id = self.ui.label.text().split(": ")[1]

        for item in self.list_ro:
            if str(item.order_id) == str(id):
                producer_name = str(item.facility_name)
                try:
                    product_name = str(item.product_name)
                except:
                    product_name = ''
                # product_id = str(item['id_product'])
                id = str(item.order_id)

        self.ui.lbl_ro_selected.setText(self.lang['btn_select']['INIT_RO_SELECT'] + id)
        self.ui.rtb_info_ro_selected.clear()
        self.ui.rtb_info_ro_selected.append(self.lang['btn_select']['PRODUCER'] + producer_name)
        if self.ui.cbb_select_machine.currentText() != self.lang['machine']['format']:
            self.ui.rtb_info_ro_selected.append(self.lang['btn_select']['PRODUCT'] + product_name)
        # self.ui.rtb_info_ro_selected.append(self.lang['btn_select']['PRODUCE_ID'] + product_id)

        self.status_machine = enum.sMachine.READY
        self.get_infomation_ro(id)

    def slot_btn_refresh_orders(self):
        self.status_machine = enum.sMachine.CHANGE_RO
        self.get_order()

    def slot_btn_close(self):
        self.ui.stackwget_action.setCurrentIndex(1)

    def slot_btn_detail_success(self):
        self.ui.stackwget_action.setCurrentIndex(2)

    def slot_btn_setup_info(self): # thông tin cá nhân
        self.ui.stackwget_setup.setCurrentIndex(0)

    def slot_btn_setup_lang(self): # cài đặt ngôn ngữ
        self.ui.stackwget_setup.setCurrentIndex(1)

    def btn_setup_stamp(self): # cài đặt thông số tem
        self.ui.stackwget_setup.setCurrentIndex(2)

    def select_machine(self): # lựa chọn loại máy sử dụng
        # self.show_loading = True
        self.get_order()


    def run_check_approving_login(self, progress_callback):
        self.flag_stop_thread["approving_login"] = True
        while(self.flag_stop_thread["approving_login"]):
            # print("check run_check_approving_login")
            username = self.ui.txt_username.text()
            password = self.ui.txt_password.text()
            url_login = ParaMachine.URL_SERVER.value + 'login'
            
            myobj = {'email': username, "password": password, "id_machine": self.ID_machine}
            try:
                x = requests.post(url_login, data = myobj)
                if(x.status_code == 200):
                    y = json.loads(x.text)
            except:
                time.sleep(1)
            else:
                status_result = y["success"]['status']
                if(status_result != 3):
                    self.ui.lbl_message_login.setText(self.lang['message_login']['APPROVALED'])
                    self.flag_stop_thread["approving_login"] = False
            finally:
                time.sleep(2)

    def slot_get_info_id(self):
        print("enter slot_get_info_id")

    def slot_set_ro_current(self):
        print("slot_set_ro_current")

    def slot_table_releaser_order(self):
        self.button_setEnable(self.ui.btn_select, True)
        self.button_setEnable(self.ui.btn_format_select, True)
        # self.button_setEnable(self.ui.btn_repair_ro, True) # tạm thời chưa có chức năng sửa lệnh phát hành trực tiếp trên máy phát hành

        r = self.ui.table_releaser_order.currentRow()
        id = self.ui.table_releaser_order.item(r,0).text()
        self.ui.label.setText(self.lang['gui']['label'] + str(id))

        for item in self.list_ro:
            if str(item.order_id) == str(id):
                producer_name = str(item.facility_name)
                product_name = str(item.product_name)
                # product_id = str(item['id_product'])
                id = str(item.order_id)
                total = str(item.total_seri)
                start = str(item.start_seri)
                current = str(item.no_number)
                status = int(item.status)
                
                if status == enum.sRO.READY.value or status == enum.sRO.PAUSE.value or status == enum.sRO.RELEASING.value:
                    self.button_setEnable(self.ui.btn_select, True)
                    self.button_setEnable(self.ui.btn_format_select, True)
                else:
                    self.button_setEnable(self.ui.btn_select, False)
                    self.button_setEnable(self.ui.btn_format_select, False)
                    
                self.ui.rtb_detail_ro.clear()
                self.ui.rtb_detail_ro.append(self.lang['btn_select']['PRODUCER'] + producer_name)
                self.ui.rtb_detail_ro.append(self.lang['btn_select']['PRODUCT'] + product_name)
                # self.ui.rtb_detail_ro.append(self.lang['btn_select']['PRODUCE_ID'] + product_id)
                self.ui.rtb_detail_ro.append(self.lang['btn_select']['PRODUCTION_ID'] + id)
                self.ui.rtb_detail_ro.append(self.lang['btn_select']['TOTAL_SERI'] + total)
                self.ui.rtb_detail_ro.append(self.lang['btn_select']['START_SERI'] + start)
                self.ui.rtb_detail_ro.append(self.lang['btn_select']['CURRENT_SERI'] + current)
                self.ui.rtb_detail_ro.append(self.lang['btn_select']['STATUS'] + str(self.statusRO[status]))

    
    def get_order(self):
        print("truoc khi order")
        waitting = True
        while waitting == True:
            self.TimerErrorNotification.cancel()
            self.button_setEnable(self.ui.btn_return, True)
            out = self.ui.cbb_select_machine.currentText() # Giá trị đang chọn 
            self.cnt_tem_error = 0
            self.ui.lbl_num_fail.setText(str(self.cnt_tem_error))
        
            self.ui.rtb_detail_ro.clear()
            self.ui.rtb_detail_ro_2.clear()

            self.button_setEnable(self.ui.btn_select, False)
            self.button_setEnable(self.ui.btn_format_select, False)
            print("khi order")
            if(out == self.lang['machine']['format']):
                print("format order")
                self.list_ro = self.formatMachine.get_order()
                self.ui.stackwget_action.setCurrentIndex(1)
                self.OrderType = OrderType.Format
                print(" sau format order")
                waitting = False
            else: #if(out == self.lang['machine']['release']): # Mặc định là chọn lệnh phát hành
                print("release order")
                self.list_ro = self.releaseMachine.get_order()
                self.ui.stackwget_action.setCurrentIndex(0)
                self.OrderType = OrderType.Release
                print(" sau release order")
                waitting = False

    def func_set_progress(self, num_comp, num_total):
        self.ui.lbl_total_success.setText(str(num_comp) + "/" + str(num_total))
        value_progress = int(num_comp * 100 / num_total)
        self.ui.progressBar.setValue(value_progress)

    # Sau khi lựa chọn lệnh phát hành sẽ hiện thị số seri tiếp theo
    def get_infomation_ro(self, id_ro):
        for item in self.list_ro:
            if str(item.order_id) == str(id_ro):
                self.number_display["order_id"] = item.order_id
                IsSelected = self.Library.SelectOder(item.order_id, self.OrderType) # CHọn lệnh phát hành từ server
                if IsSelected:
                    self.selected_ro = item # Lưu thông tin ro đang chọn

                    if(self.OrderType == OrderType.Release):
                        start_seri_server = item.start_seri # Số seri bắt đầu
                        total_number_stamps = item.total_seri # tổng số tem của lệnh
                        current_number_stamps = item.no_number #Số thứ tự tem hiện tại

                        seri_curent = start_seri_server + current_number_stamps
                        self.number_display["start_seri"] = start_seri_server #  int(str(seri_curent))
                        self.number_display["num_seri_cur"] = seri_curent #  int(str(seri_curent))
                        self.number_display["num_success"] = self.number_display["number_cur"]   = current_number_stamps
                        seri_curent = (str(self.number_display["num_seri_cur"]))

                        self.ui.lbl_num_success.setText(str(self.number_display["num_success"]))
                        self.ui.lbl_numberSeri.setText(seri_curent)
                        
                        self.func_set_progress(current_number_stamps, total_number_stamps)
                    
                    elif(self.OrderType == OrderType.Format):
                        total_number_stamps = item.total_number # tổng số tem của lệnh
                        current_number_stamps = item.no_number #Số thứ tự tem hiện tại

                        self.number_display["num_success"] = self.number_display["number_cur"]   = current_number_stamps

                        self.ui.lbl_num_success.setText(str(self.number_display["num_success"]))
                        self.ui.lbl_numberSeri.setText("")
                        self.func_set_progress(current_number_stamps, total_number_stamps)
                else:
                    print('không chọn được lệnh phát hành')
    

