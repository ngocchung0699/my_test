from GPIO.DefineParameter import ParaSensorMetal
import RPi.GPIO as GPIO

from GPIO.DefinePin import *

from Features.DEvent import DEvent

from Features.DTimer import DTimer
import time

class Sensor():
    DetectMetal = DEvent()#detect kim loai

    def __init__(self):
        super().__init__()
        self.count_Sensor = 0
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #Set pins active
        GPIO.setup(PinSensorMetal, GPIO.IN, pull_up_down= GPIO.PUD_UP)

        self.timer = DTimer(ParaSensorMetal.TimeResponse.value, self.__ReadSensor)
        self.timer.start()

    def __ReadSensor(self):
        self.__ReadSensorMetal()

    def StopReadSensor(self):
        self.timer.cancel()

    def __ReadSensorMetal(self):
        if GPIO.input(PinSensorMetal) == ParaSensorMetal.PositiveLevel.value:
            self.count_Sensor +=1
            if self.count_Sensor == ParaSensorMetal.AntiJamming.value:
                self.DetectMetal.emit()        
        else :
            self.count_Sensor = 0

if __name__ == "__main__":
    def ViewSensor():
        print('ok DQD')

    sensor = Sensor()
    sensor.DetectMetal.connect(ViewSensor)
    while True:
        pass

   