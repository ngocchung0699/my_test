import types
import typing


class DEvent:
    def __init__(self, *types: typing.Any):
        self.types = types 
        self.callbacks = list()

    def connect(self, callback: types.FunctionType):
        '''Thêm func để xử lý event'''
        self.callbacks.append(callback)

    def disconnect(self, callback: types.FunctionType):
        '''Xóa bỏ func xử lý event nếu không dùng tới nữa'''
        self.callbacks.remove(callback)

    def emit(self,  *args: typing.Any):
        '''Gọi event cần thực hiện'''

        if len(self.types) != len(args):
            raise TypeError('signal has %s argument(s) but %s provided' % (len(self.types), len(args)))

        for ii in range(len(self.types)):
            if type(args[ii]) != self.types[ii]:
                raise Exception("argument %s must be of type %s, not of type %s" %(ii + 1, self.types[ii], type(args[ii])) )

        #Call func có trong list
        for callback in self.callbacks:
            callback(*args)