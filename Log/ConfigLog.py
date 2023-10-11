from asyncio import streams
from asyncio.log import logger
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import FileHandler, Formatter, StreamHandler

from src.utils import get_project_root

# Mức	    Nội dung
# DEBUG	    Thông tin chi tiết, thường là thông tin để tìm lỗi
# INFO	    Thông báo thông thường, các thông tin in ra khi chương trình chạy theo đúng kịch bản
# WARNING	Thông báo khi nghi vấn bất thường hoặc lỗi có thể xảy ra, tuy nhiên chương trình vẫn có thể hoạt động
# ERROR	    Lỗi, chương trình có thể không hoạt động được một số chức năng hoặc nhiệm vụ nào đó, thường thì nên dùng ghi bắt được Exception
# CRITICAL	Lỗi, chương trình gặp lỗi nghiêm trọng không thể giải quyết được và bắt buộc phải dừng lại

# Bật tắt logging.
# Nếu không cần đến logging –> tắt chế độ ghi log:
# logger.disabled = True

# Khi cần bật lại:
# logger.disabled = False

class ConfigLog():
    logger = logging.getLogger('ConfigLog')

    path_log = get_project_root() + '/Log/'
    def StartBasic():
        logging.basicConfig(
            filename= ConfigLog.path_log + 'LogProcess/Process.log', 
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] - %(message)s',
            filemode='w')

    #Thực hiện lưu log nhieu noi
    def StartHandlers(self):
        self.logger.setLevel(logging.DEBUG)
        formatter = Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] - %(message)s')

        #file handles - lưu log vào 1 file
        file_handler = FileHandler(ConfigLog.path_log + 'LogProcess/Process.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


        #stream handles - lưu log vào console
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    #Lưu log có tách file theo dung lượng
    def StartRotateHandlers(self, maxBytes=5000000, backupCount=20):
        self.logger.setLevel(logging.DEBUG)
        formatter = Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] - %(message)s')

        #file handles - lưu log vào 1 file
        #maxBytes- dung lượng tối đa của 1 file. VD: > 2000B sẽ tách sang file khác
        #backupCount- số file tối đa có the lưu thêm. VD: 10
        file_handler = RotatingFileHandler(ConfigLog.path_log + 'LogProcess/Process.log', maxBytes=maxBytes, backupCount=backupCount)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        file_handler = RotatingFileHandler(ConfigLog.path_log + 'LogHisCheck/HisCheck.log', maxBytes=maxBytes, backupCount=backupCount)
        file_handler.setLevel(logging.CRITICAL)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        #stream handles - lưu log vào console
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    #tách file log theo thời gian
    def StartTimeRotateHandlers(self, when='midnight', interval=1, backupCount= 30):
        self.logger.setLevel(logging.DEBUG)
        # formatter = Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] - %(message)s')
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

        #file handles - lưu log vào 1 file
        # when trong TimedRotatingFileHandler có thể nhận các giá trị sau:
        # second (s)
        # minute (m)
        # hour (h)
        # day (d)
        # w0-w6 (weekday, 0=Monday)
        # midnight
        file_handler = TimedRotatingFileHandler(ConfigLog.path_log + 'LogProcess/Process.log', when=when, interval=interval, backupCount = backupCount)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # #log crash app
        # file_handler = TimedRotatingFileHandler(ConfigLog.path_log + 'LogCritical/Critical.log', when=when, interval=interval)
        # file_handler.setLevel(logging.CRITICAL)
        # file_handler.setFormatter(formatter)
        # self.logger.addHandler(file_handler)

        # #log warning app
        # file_handler = TimedRotatingFileHandler(ConfigLog.path_log + 'LogWarning/Warning.log', when=when, interval=interval)
        # file_handler.setLevel(logging.WARNING)
        # file_handler.setFormatter(formatter)
        # self.logger.addHandler(file_handler)

        #log crash app
        file_handler = TimedRotatingFileHandler(ConfigLog.path_log + 'LogMotor/Motor.log', when=when, interval=interval)
        file_handler.setLevel(logging.CRITICAL)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        #stream handles - lưu log vào console
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

# if __name__ == '__main__':
#     # ConfigLog.StartBasic()
#     cl = ConfigLog()
#     cl.StartHandlers()
#     ConfigLog.logger.debug('This is a debug log message.')
#     ConfigLog.logger.info('This is a info log message.')
#     ConfigLog.logger.warning('This is a warning log message.')
#     ConfigLog.logger.error('This is a error log message.')
#     ConfigLog.logger.critical('This is a critical log message.')