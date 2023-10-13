
from GPIO.DefineParameter import ParaStepMotor
import RPi.GPIO as GPIO
import time
from GPIO.DefinePin import *

# from DefineParameter import ParaStepMotor
# import RPi.GPIO as GPIO
# import time
# from DefinePin import *

# Variables
class StepMotor:
    def __init__(self, PinDirection, PinStep, PinEnable):
        super().__init__()

        self.Microsteps = 360 / ParaStepMotor.StepAngle.value  #Số Vi bước cần thực hiện để quay hết 1 vòng-Ví dụ StepAngle=1.8 -> cần 200 Fulse mới quay hết 1 vòng

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.PinDirection   = PinDirection
        self.PinStep        = PinStep
        self.PinEnable      = PinEnable
        #Set pins active
        GPIO.setup(self.PinDirection, GPIO.OUT)
        GPIO.setup(self.PinStep, GPIO.OUT)
        GPIO.setup(self.PinEnable, GPIO.OUT)

        self.freq = 2000
        self.duty = 50
        self.DC_pwm = GPIO.PWM(self.PinStep, self.freq)
        self.DC_pwm.stop()
    def __exit__(self):
        self.Disable()
        GPIO.cleanup()

    def Disable(self):
        self.Stop()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PinEnable, GPIO.OUT)
        GPIO.output(self.PinEnable, True)

    def Enable(self):
        GPIO.output(self.PinEnable, False)
        self.DC_pwm.start(0)

    #quay cùng chiều kim đồng hồ
    def DirClockwise(self):
        GPIO.output(self.PinDirection, False)

    #quay ngược chiều kim đồng hồ
    def DirCounterClockwise(self):
        GPIO.output(self.PinDirection, True)

    def Run(self):
        self.DC_pwm.ChangeFrequency(1/self.freq)
        self.DC_pwm.ChangeDutyCycle(self.duty)

    def SetSpeed(self, speed = 20):
        self.duty = 50
        self.freq = 60*0.0625*3/(10*speed*self.Microsteps)
        # print("self.freq", self.freq)

    def Stop(self):
        self.DC_pwm.stop()

if __name__ == "__main__":
    motorLeft = StepMotor(PinDirection= PinDirectionLeft, PinEnable= PinEnableLeft, PinStep= PinStepLeft)
    motorRight = StepMotor(PinDirection= PinDirectionRight, PinEnable= PinEnableRight, PinStep= PinStepRight)

    time.sleep(1)
    motorLeft.Disable()
    motorRight.SetSpeed(20)
    motorRight.Enable()
    motorRight.DirCounterClockwise()
    motorRight.Run()
    time.sleep(20)
    # motorRight.Disable()
    # motorLeft.SetSpeed(20)
    # motorLeft.Enable()
    # motorLeft.DirClockwise()
    # motorLeft.Run()
    # time.sleep(3)
    # motorLeft.Disable()
    
    motorLeft.__exit__()
    motorRight.__exit__()

