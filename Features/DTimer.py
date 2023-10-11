from threading import Timer
import time

class DTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


if __name__ == "__main__":
    def dummyfn(msg="foo"):
        print(msg)

    timer = DTimer(0.1, dummyfn, args=[3])
    timer.start()
    for i in range(10):
        print('dqd')
        time.sleep(1)
    timer.cancel()