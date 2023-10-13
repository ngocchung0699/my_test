import threading
from GPIO.DefineParameter import ParaButton
import RPi.GPIO as GPIO
from GPIO.DefinePin import *
from Features.DEvent import DEvent
from Features.DTimer import DTimer

# import time
# import threading
# from DefineParameter import ParaButton
# import RPi.GPIO as GPIO
# from DefinePin import *
# from DEvent import DEvent
# from DTimer import DTimer

class Button:
    DetectButton = DEvent()#detect nut bam
    def __init__(self, PinButton, PinLed):

        self.PinButton = PinButton
        self.PinLed = PinLed
        self.cntButton = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #Set pins active
        GPIO.setup(self.PinButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.PinLed, GPIO.OUT)

        GPIO.output(self.PinLed, False)

        self.timer = DTimer(ParaButton.TimeResponse.value, self.CheckButton)
        self.timer.start()

        self.StatusButton = 0
        self.isCheck = True

    def Busy(self):
        if self.StatusButton == 0:
            return False
        else:
            return True
    def allowCheck(self, value):
        self.isCheck = value
    def SetClickButton(self, value):
        self.StatusButton = value
    def ClickButton(self):
        return self.StatusButton
    def LedButton(self, status):
        GPIO.output(self.PinLed, status)
    def read_button(self):
        return GPIO.input(self.PinButton)
    def CheckButton(self):
        if self.isCheck == True:
            if GPIO.input(self.PinButton) == ParaButton.PositiveLevel.value:
                self.cntButton = self.cntButton + 1
                if self.cntButton == ParaButton.AntiJamming.value:
                    if self.StatusButton == 0:
                        self.StatusButton = 1
                    else:
                        self.StatusButton = 0 
                    self.DetectButton.emit()    
            else:
                self.cntButton = 0
    
    def StopReadButton(self):
        self.timer.cancel()

    def __del__(self):
        GPIO.output(self.PinLed, False)
        GPIO.cleanup()
if __name__ == "__main__":
        #init button
    print("testing")
    buttonLeft = Button(PinButton = PinButtonLeft, PinLed = PinLedLeft)
    buttonRight = Button(PinButton = PinButtonRight, PinLed = PinLedRight)

    def ProcessButtonLeft():
        if buttonRight.Busy() == False:
            if buttonLeft.ClickButton()== 1:
                buttonLeft.LedButton(1)
                buttonLeft.SetClickButton(2)
                buttonRight.allowCheck(False)
                # motorRight.Disable()
                # motorLeft.Enable()
                # motorLeft.DirClockwise()
                # motorLeft.RunAsyn(-1)
            if buttonLeft.ClickButton()== 0:
                buttonLeft.LedButton(0)
                buttonRight.allowCheck(True)
                # motorLeft.Disable()

    def ProcessButtonRight():
        if buttonLeft.Busy() == False:
            if buttonRight.ClickButton() == 1:
                buttonRight.LedButton(1)
                buttonRight.SetClickButton(2)
                buttonLeft.allowCheck(False)
                # motorLeft.Disable()
                # motorRight.Enable()
                # motorRight.DirClockwise()
                # motorRight.RunAsyn(-1)
            if buttonRight.ClickButton() == 0:
                buttonRight.LedButton(0)
                buttonLeft.allowCheck(True)
                # motorRight.Disable()
        
    buttonLeft.DetectButton.connect(ProcessButtonLeft)
    buttonRight.DetectButton.connect(ProcessButtonRight)

    while(1):
        pass

