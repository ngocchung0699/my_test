import types

#Callback
def fnBookUber(objUser):
    print('Inside fbBookUber()')

class myEvent:
    def __init__(self, *args):
        self.callbacks = list()

    def registerCallback(self, callback: types.FunctionType):
        self.callbacks.append(callback)

    def call(self, objUser):
        print('Kích hoạt sự kiện')

        for callback in self.callbacks:
            callback(*args)

if __name__ == "__main__":
    myEvent = myEvent()

    #Registration
    myEvent.registerCallback(fnBookUber)

    #Calling/Firing the event
    # myEvent.call(1)