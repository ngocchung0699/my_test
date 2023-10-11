import RPi.GPIO as GPIO
import time
from GPIO.DefinePin import *

class Buzzer:
    def __init__(self, PinBuzzer):
        self.PinBuzzer = PinBuzzer
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) 
        GPIO.setup(self.PinBuzzer, GPIO.OUT)
        GPIO.output(self.PinBuzzer, False)
    def Enable(self):
        GPIO.output(self.PinBuzzer, True)
    def Disable(self):
        GPIO.output(self.PinBuzzer, False)
    def __exit__(self):
        self.Disable()
        GPIO.cleanup()
    def __del__(self): 
        self.Disable()
        GPIO.cleanup()

if __name__ == "__main__":
    Buzz = Buzzer(PinBuzzer = PinBuzzer)
    Buzz.Enable()
    time.sleep(2)
    Buzz.Disable()
    time.sleep(2)
    Buzz.__exit__()

