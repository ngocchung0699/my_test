import configparser
from pathlib import Path

class Properties():
    def __init__(self):
        super().__init__()
        self.pathConfig = str(Path(__file__).parent.parent) + "\ini\ConfigDevice.ini"
        print(self.pathConfig)

        self.Config = configparser.ConfigParser()

        self.SECTION_PARAMETER = 'DEFAULT'

    #Token đăng nhập
    @property
    def Token(self):
        return self.__LoadConfig('Token')
    @Token.setter
    def Token(self, value:str):
        self.__SaveConfig('Token', value)

    #thông tin tài khoản đăng nhập
    @property
    def InfoUser(self):
        return self.__LoadConfig('InfoUser')
    @InfoUser.setter
    def InfoUser(self, value:str):
        self.__SaveConfig('InfoUser', value)

    #thông tin lệnh phát hành
    @property
    def ReleaseOrders(self):
        return self.__LoadConfig('ReleaseOrders')
    @ReleaseOrders.setter
    def ReleaseOrders(self, value:str):
        self.__SaveConfig('ReleaseOrders', value)


    # ------------------------------------------------------------- start ĐỌC/GHI dữ liệu vào local -------------------------------------------------------------
    def __LoadConfig(self, option:str):
        try: #Lấy dữ liệu của 1 trường thông tin
            self.Config.read(self.pathConfig, encoding="utf-8")
            _data = self.Config.get(self.SECTION_PARAMETER, option)
            if _data == '':
                return None
            else:
                return _data
        except: #Nếu chưa có trường thông tin này thì thêm mới và trả về None
            self.__SaveConfig(option, None)
            return None

    def __SaveConfig(self, option:str, value:str):
        if value == None:
            value = ''
        self.Config.read(self.pathConfig, encoding="utf-8")
        self.Config.set(self.SECTION_PARAMETER, option, value)

        with open(self.pathConfig, 'w', encoding="utf-8") as configfile:
            self.Config.write(configfile)
    # ------------------------------------------------------------- end ĐỌC/GHI dữ liệu vào local -------------------------------------------------------------


if __name__ == '__main__':
    pro = Properties()
    pro.Token = 'dqd xin chào q'
    # pro.InfoUser = 'dqd xin chào adqđq'
    print(pro.ReleaseOrders)
