from GPIO.Sensor import Sensor

if __name__ == "__main__":
    def ViewSensor():
        print('ok DQD')

    sensor = Sensor()
    sensor.DetectMetal.connect(ViewSensor)
    while True:
        pass
