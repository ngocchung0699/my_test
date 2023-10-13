#Sử dụng thư viện iStamp.dll - chỉ sử dụng dược python trên window

import json
import sys
from typing import List
import clr
from pathlib import Path


from GPIO.DefineParameter import ParaMachine
from Database.Models.UserInfoModel import UserInfoModel

system = ParaMachine.SYSTEM.value
if system == 'win32':
    # sys.path.append(r"E:\Stech\GitHub\onyxvietnam\TrueOrigin\TrueOrigin.iStamp\TrueOrigin.iStamp\bin\Release\netstandard2.0")
    sys.path.append(str(Path(__file__).parent.parent) +  "/Libraries/iStamp")
elif system == 'linux':
    sys.path.append(str(Path(__file__).parent.parent) +  "/Libraries/iStamp")
    from Libraries.CardTransceive import CardTransceive


clr.AddReference("TrueOrigin.iStamp")

from TrueOrigin.iStamp.Api.Model import ConfigApi
from TrueOrigin.iStamp.Converters import  IDebug, iStampDebug, JsonConverter
from TrueOrigin.iStamp.Services import IDevice
from TrueOrigin.iStamp.Models import SealerInfo 
from TrueOrigin.iStamp.Functions import Sealer
from TrueOrigin.iStamp.Define import TagCommand, DefCode, Stamp, StampInfo, stamp_version
from System import Byte, Array, Enum, Type

from TrueOrigin.iStamp.Api import ApiGetConfig, ApiAccount, ApiStampRelease, ApiStampFactory, ApiStampSpecifications
from TrueOrigin.iStamp.Api.Model.Account import LoginMethod, PermissionsType
from TrueOrigin.iStamp.Api.Model.StampRelease import OrderReleaseModel, ProductType
from TrueOrigin.iStamp.Api.Model import ApiCode
from Database.ini.Properties import Properties

sys.path.append(str(Path(__file__).parent.parent) + "/Database/DQD_EntityFrameworkCore/Repository")
from VariableRepository import VariableRepository
from OrderReleaseRepository import OrderReleaseRepository
from OrderFactoryRepository import OrderFactoryRepository
from UserRepository import UserRepository
from StampSpecificationsRepository import StampSpecificationsRepository
from StampSpecificationsModel import StampSpecificationsModel


# Việc khai báo thêm OrderReleaseModel chỉ giúp việc gợi ý lệnh trở nên thuận tiện hơn
# Thực tế không cần khai báo này
from OrderReleaseModel import OrderReleaseModel 
from OrderFactoryModel import OrderFactoryModel

class debug(IDebug):
    __namespace__ = "iStamp.Converters"

    def WriteLine(self,  *args):
        if len(args) >1:
            print(args[0].format(str(args[1])))
        else:
            print(args[0])

class ResultLogin(Enum):
    LoginSuccess    = 0 # đăng nhập thành công
    LoginFailed     = 1 # đăng nhập thất bại
    NoAccess        = 2 # tài khoản không có quyền truy cập ứng dụng

class MachineFunc(Enum):
    NoFunc                  = 0 # máy không có chức năng gì
    ReleaseMachine          = 1 # máy có chức năng phát hành
    FormatMachine           = 2 # máy có chức năng format
    MultiFuncMachine        = 3 # máy có nhiều chức năng

class OrderType(Enum): #Loại lệnh là xuất xưởng/phát hành
    NoneType    = 0
    Release     = 1 # lệnh phát hành
    Format      = 2 # Lệnh xuất xưởng

class DeviceTest(IDevice): # Giả lập ra 1 Device với dữ liệu tem ảo để test thư viện
    __namespace__ = "iStamp.Services"
    SamplesTag = [  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x1C, 0xD1, 0x01, 0x18, 0x55, 0x04, 0x74, 0x72, 0x75, 0x65, 0x6F, 0x72, 0x69, 0x67, 0x69, 0x6E, 0x2E, 0x69, 0x6E, 0x66, 0x6F, 0x2F, 0x31, 0x32, 0x33, 0x34, 0x35, 0x35, 0x36, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0xD6, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x66, 0x84, 0x4E, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0E, 0x80, 0x00, 0x00, 0x00, 0x0D, 0x66, 0x84, 0x4E, 0x66, 0xDA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x1C, 0xD1, 0x01, 0x18, 0x55, 0x04, 0x74, 0x72, 0x75, 0x65, 0x6F, 0x72, 0x69, 0x67, 0x69, 0x6E, 0x2E, 0x69, 0x6E, 0x66, 0x6F, 0x2F, 0x31, 0x32, 0x33, 0x34, 0x35, 0x35, 0x36, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0xD6, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x66, 0x84, 0x4E, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0E, 0x80, 0x00, 0x00, 0x00, 0x0D, 0x66, 0x84, 0x4E, 0x66, 0xDA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x1C, 0xD1, 0x01, 0x18, 0x55, 0x04, 0x74, 0x72, 0x75, 0x65, 0x6F, 0x72, 0x69, 0x67, 0x69, 0x6E, 0x2E, 0x69, 0x6E, 0x66, 0x6F, 0x2F, 0x31, 0x32, 0x33, 0x34, 0x35, 0x35, 0x36, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0xD6, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x66, 0x84, 0x4E, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0E, 0x80, 0x00, 0x00, 0x00, 0x0D, 0x66, 0x84, 0x4E, 0x66, 0xDA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x1C, 0xD1, 0x01, 0x18, 0x55, 0x04, 0x74, 0x72, 0x75, 0x65, 0x6F, 0x72, 0x69, 0x67, 0x69, 0x6E, 0x2E, 0x69, 0x6E, 0x66, 0x6F, 0x2F, 0x31, 0x32, 0x33, 0x34, 0x35, 0x35, 0x36, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0xD6, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x66, 0x84, 0x4E, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0E, 0x80, 0x00, 0x00, 0x00, 0x0D, 0x66, 0x84, 0x4E, 0x66, 0xDA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    def Transceive(self,  data):
        # Mô phỏng lại thẻ NFC bằng cách lấy ra 1 mảng giả BytesTag, thao tác đọc/ghi sẽ được thực hiện trên mảng giả này
    
        GetInfoTag = 0x60  # cmd get info tag
        ReadUIDcard = 0x00 #cmd get uid card
        if (data[0] == GetInfoTag):
            return Array[Byte](bytearray([0x00, 0x04, 0x04, 0x02, 0x01, 0x00, 0x0F, 0x03]))

        elif (data[0] == TagCommand.READ and data[1] == ReadUIDcard):
            return Array[Byte](bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08 ])) #trả về UID

        elif (data[0] == TagCommand.PWD_AUTH):
            return Array[Byte](bytearray([0x66, 0xDA]))#với UID trên sẽ tạo ra được mã xác thực như vậy
            
        elif (data[0] == TagCommand.READ):
            IndexPage = (data[1] * 4)
            reponse =  bytearray(16)

            for ii in range(IndexPage, IndexPage + 16):
                reponse[ii - IndexPage] = self.SamplesTag[ii] #lệnh đọc sẽ trả về 16byte của mảng

            return Array[Byte](bytearray(reponse))

        elif (data[0] == TagCommand.WRITE):
            IndexPage = data[1] * 4

            for ii in range(0,4):
                self.SamplesTag[IndexPage + ii] = data[ii + 2] # lệnh ghi sẽ ghi các bytes vào mảng mô phỏng
            return Array[Byte](bytearray([0x0A]))

        return Array[Byte](bytearray(data))

class Device(IDevice): # Kế thừa Interface Device thật
    __namespace__ = "iStamp.Services"
    def Transceive(self,  data):
        if system == 'linux':
            return LibHandling.cardTransceive.Transceive(data)
        pass

    def EndSession(self, IsScanSuccess):
        pass

class LibHandling():
    def __init__(self):
        super().__init__()

        if system == 'win32':
            LibHandling.cardTransceive = None
        elif system == 'linux':
            LibHandling.cardTransceive = CardTransceive()

        # iStampDebug.Init(debug()) # init Debug- Mỗi ứng dụng cần khởi tạo trình debug của riêng nó để có thể chạy debug ở trong thư viện

        self.SealerInfo = SealerInfo()
        self.SealerInfo.Device  = Device()
        
        self.SealerInfo.Location= None
        self.SealerInfo.Token   = "free"
        self.SealerInfo.LinkApiOriginal = "http://192.168.1.205/stech/temchip/public/" #
        # self.SealerInfo.LinkApiOriginal = "https://trueorigin.info/"
        # self.SealerInfo.LinkApiOriginal = "http://103.229.41.231/onyx/temchip/public/"
        
        print('ConfigApi.UrlApiConfig: ', ConfigApi.UrlStorage)
        data = ApiGetConfig.GetConfigApp() # Lấy cấu hình từ server(link api, ....)
        data.Wait()
        response = data.Result

        self.Sealer = None # Khai báo thiết bị là 1 Sealer- Tuy nhiên chưa khởi tạo sealer này, khi nào login thành công mới khởi tạo

        # self.properties = Properties() # Sử dụng datalocal ini
        # self.properties = SqlLiteHandling() # Sử dụng datalocal SqlLite
        self.properties = VariableRepository()# Sử dụng datalocal SqlLite theo Entity
        self.order_release = OrderReleaseRepository()
        self.order_factory = OrderFactoryRepository()
        self.user = UserRepository()
        self.stamp_spec = StampSpecificationsRepository()
        
    def Login(self, username:str, password:str) :
        '''đăng nhập và kiểm tra xem tài khoản có quyền truy cập ứng dụng hay không. 
        Trả về kết quả đăng nhập'''
 
        data = ApiAccount.Login(LoginMethod.trueorgin, username, password, "", "")
        data.Wait() 
        response = data.Result
        if response == None:
            return ResultLogin.LoginFailed, None
        else:
            for per in response.Permissions:
                # Máy phát hành nên chỉ kiểm tra xem có quyền phát hành tem hoặc quyền format tem hay không?
                if per == PermissionsType.release_order_releasing or per == PermissionsType.stamp_format_ro_releasing : 
                    self.properties.Token = response.Token # lưu token vào local
                    #Nếu đăng nhập thành công thì khởi tạo Sealer để có thể thực hiện phát hành tem
                   
                    self.SealerInfo.Username= username
                    self.Sealer = Sealer(self.SealerInfo, False) # máy phát hành tem, nên chỉ khởi tạo Sealer và không cần kết nối với SealCore
                    
                    #Kiểm tra xem máy có chức năng gì, phát hành hay format hoặc cả 2 chức năng.
                    if PermissionsType.release_order_releasing in response.Permissions and PermissionsType.stamp_format_ro_releasing in response.Permissions :
                        return ResultLogin.LoginSuccess, MachineFunc.MultiFuncMachine
                    else:
                        if PermissionsType.release_order_releasing in response.Permissions:
                            return ResultLogin.LoginSuccess, MachineFunc.ReleaseMachine
                        if PermissionsType.stamp_format_ro_releasing in response.Permissions:
                            return ResultLogin.LoginSuccess, MachineFunc.FormatMachine
                            
            return ResultLogin.NoAccess, MachineFunc.NoFunc
    
    
    def Logout(self): #
        '''Đăng xuất tài khoản, 
        trả về true/false'''
        data = ApiAccount.Logout(self.properties.Token)
        data.Wait() 
        response = data.Result
        return response


    def GetInfo(self): #
        '''lấy thông tin user. trả về UserModel'''
        data = ApiAccount.GetInfo(self.properties.Token)
        data.Wait() 
        response = data.Result
        if response is not None:
            data_str = JsonConverter.Dumps(response, IsIgnoreNullValue = False)
            # Bỏ qua trường facilities
            data_obj1 = json.loads(data_str)
            data_obj1['facilities'] = None
            data_str1 = json.dumps(data_obj1).replace('"facilities": null,', '')
            #-------------------------------------------------------------------------
            data_obj = json.loads(data_str1, object_hook=lambda d: UserInfoModel(**d))
            self.user.Update(data_obj)
        return response

    # Các api liên quan lệnh xuất xưởng
    def GetAllOrdersFactory(self):
        '''Lấy tất cả orders của tài khoản này'''
        data = ApiStampFactory.GetAllOrders(self.properties.Token)
        data.Wait() 
        response = data.Result

        self.__UpdateListOrdersFactoryLocal(response)
        # return json.loads(result_str, object_hook=lambda d: OrderReleaseModel(**d))
        return response
    
    def CheckUid(self, orderId: int, uid:int):
        '''Kiểm tra xem uid có hợp lệ hay không?'''
        data = ApiStampFactory.CheckUid(self.properties.Token, orderId, uid)
        data.Wait() 
        response = data.Result
        return response
    
    def UpdateSeriFormated(self, orderId: int, uid:int) -> bool: # 
        '''cập nhật số xuất xưởng thành công cho Server'''
        data = ApiStampFactory.UpdateSeriReleased(token= self.properties.Token, OderId= orderId, uid= uid)
        response = data.Result
        return response

    def FormatStamp(self, order_format: OrderFactoryModel):
        ''' Format tem
        <returns>
                True: nếu format thành công \r\n
                ApiCode: nếu format thất bại, báo lỗi cụ thể của ApiCode \r\n
                None: nếu lệnh format này đã hoàn thành
        </returns>'''
        #kết nối với tem và format
        uid = LibHandling.cardTransceive.TryConnect()
        print("FormatStamp uid--------------", uid)
        if uid is not False:
            resultFormat = self.Sealer.FactoryReset(self.properties.Token, uid, order_format)
            stamp = resultFormat.Item1
            order_format = resultFormat.Item2
            # print("FormatStamp Status: " + stamp.Result)
            if stamp.Result == DefCode.FactoryResetOK:
                return True, order_format.no_number
            elif stamp.Result == DefCode.FactoryResetComplete: # Hoàn thành lệnh format
                # print("FormatStamp Complete")
                return None,order_format.no_number
            else:
                return stamp.Result.ToString(), ""
        else:
            print('NFC Connect Err')
            return "UnknownError", ""
    # END - api lệnh xuất xưởng

    # Các api liên quan lệnh phát hành
    def GetAllOrders(self) -> List[OrderReleaseModel]: #
        '''Lấy tất cả orders của tài khoản này'''
        data = ApiStampRelease.GetAllOrders(self.properties.Token)
        data.Wait() 
        response = data.Result

        self.__UpdateListOrdersLocal(response)
        # return json.loads(result_str, object_hook=lambda d: OrderReleaseModel(**d))
        return response

    def SelectOder(self, orderId:int, orderType:OrderType) -> bool: # 
        if(orderType == OrderType.Release):
            '''chọn 1 lệnh phát hành'''
            data = ApiStampRelease.SelectOrder(self.properties.Token, orderId)
            data.Wait() 
            response = data.Result
            return response
        elif(orderType == OrderType.Format): 
            '''chọn 1 lệnh xuất xưởng'''
            data = ApiStampFactory.SelectOrder(self.properties.Token, orderId)
            data.Wait() 
            response = data.Result
            return response
        else:
            return False

    def UnSelectOder(self, orderId:int, orderType:OrderType) -> bool: # 
        if(orderType == OrderType.Release):
            '''bỏ chọn 1 lệnh phát hành'''
            data = ApiStampRelease.UnSelectOrder(self.properties.Token, orderId)
            data.Wait() 
            response = data.Result
            return response
        elif(orderType == OrderType.Release): 
            '''bỏ chọn 1 lệnh xuất xưởng'''
            data = ApiStampFactory.UnSelectOrder(self.properties.Token, orderId)
            data.Wait() 
            response = data.Result
            return response
        else:
            return False

    def StopOder(self, orderId:int, orderType:OrderType) -> bool: #
        if(orderType == OrderType.Release):
            ''' Dừng hẳn 1 lệnh phát hành - không phải tạm dừng'''
            data = ApiStampRelease.StopOrder(self.properties.Token, orderId)
            data.Wait() 
            response = data.Result
            return response
        elif(orderType == OrderType.Release): 
            '''Dừng hẳn 1 lệnh xuất xưởng - không phải tạm dừng'''
            data = ApiStampFactory.StopOrder(self.properties.Token, orderId)
            data.Wait() 
            response = data.Result
            return response
        else:
            return False

    
    def ReleaseStamp(self, order_release: OrderReleaseModel):
        '''Phát hành tem dựa theo thông tin Server trả về \r\n
        <param name="order_release"> Thông tin của lệnh phát hành đang chọn</param> \r\n
        <returns>
                True: nếu phát hành thành công \r\n
                ApiCode: nếu phát hành thất bại, báo lỗi cụ thể của ApiCode \r\n
                None: nếu lệnh phát hành này đã hoàn thành
        </returns> '''
        
        #kết nối với tem và phát hành
        uid = LibHandling.cardTransceive.TryConnect()
        if uid is not False:
            ReleasingNumber = self.__GetSeriReleasedLocal(order_release.order_id)
            print("ReleasingNumber Get:", ReleasingNumber)
            if(ReleasingNumber):
                order_release.releasing_number = ReleasingNumber
            else:
                order_release.releasing_number = 0

            resultRelease = self.Sealer.Release(self.properties.Token, uid, order_release)
            apiCode = resultRelease.Item1
            stamp = resultRelease.Item2
            order = resultRelease.Item3
            # print('ReleaseStamp apiCode: ', apiCode)
            if stamp.Result == DefCode.ReleaseOK:
                self.__SetSeriReleasedLocal(order.order_id, "") # Xóa bỏ số đang phát hành dở trong order này, nếu có
                return True, order.no_number
            elif stamp.Result == DefCode.ReleaseComplete: # Hoàn thành lệnh phát hành

                return None, order.no_number
            else:
                #  3 điều kiện:
                #  1. Không phải lỗi Uid từ bước get No_number- Nếu lỗi từ bước này thì số no_number chưa được lấy => không cần lưu
                #  2. Lỗi này phải phát sinh từ việc tem đang cần phát hành không hợp lệ - thì mới lưu số No_number để phát hành cho lần sau
                #  3. Lỗi UnknownError của apiCode được hiểu là lỗi do quá trình ghi tem thất bại, Nên cũng tính là Lỗi cần lưu lại số seri
                # print("stamp.Result:",stamp.Result)
                # print("apiCode",apiCode)
                if(stamp.Result != DefCode.uid_invalid and (apiCode == ApiCode.UnknownError or apiCode == ApiCode.RoUidNotFound or apiCode == ApiCode.RoUidExisted or apiCode == ApiCode.RoStampNotBelongCompany)): 
                    self.__SetSeriReleasedLocal(order.order_id, order.no_number) # Lưu lại số seri lỗi để lần sau phát hành lại
                    # print("ReleasingNumber Set:", order.no_number)
                return  apiCode.ToString(), ""
        else: 
            print('NFC Connect Err')
            return "UnknownError", ""

    def GetStampBatchParameter(self) ->List[StampSpecificationsModel]: 
        '''Lấy tất cả các loại lô tem khác nhau hiện có'''
        data = ApiStampSpecifications.GetAllStampBatchParameter(token= self.properties.Token)
        data.Wait() 
        response = data.Result
        if response is not None: # Nếu có dữ liệu từ Server
            data_str = JsonConverter.Dumps(response, IsIgnoreNullValue = False)
            data_obj = json.loads(data_str, object_hook=lambda d: StampSpecificationsModel(**d))
            for item in data_obj: # Lưu tất cả dữ liệu lấy được vào local
                self.stamp_spec.Update(item)
            return data_obj
        else: # Nếu không có dữ liệu trên server thì lấy dữ liệu trong sql local
            return self.stamp_spec.GetAll()

    #----------------------------------------------------------------- START Hàm Private -------------------------------------------------------------------------------------------
    # Các lệnh sản xuất
    def __UpdateListOrdersLocal(self, response = None) -> bool: #
        ''' Cập nhật danh sách lệnh phát hành vào local'''
        if response is None:
            return

        data_str = JsonConverter.Dumps(response, IsIgnoreNullValue = False)
        data_obj = json.loads(data_str, object_hook=lambda d: OrderReleaseModel(**d))
        for item in data_obj: # Cập nhật tất cả ds orders vào csdl
            self.order_release.Update(item)


    def __GetSeriReleasedLocal(self, order_id:int) -> int: # 
        '''Get 1 số seri đã phát hành thành công trong csdl'''
        order : OrderReleaseModel = self.order_release.GetOneById(order_id= order_id)
        if order is not None:
            return order.releasing_number
        else:
            return None

    def __SetSeriReleasedLocal(self, order_id:int, no_number:int) -> bool: #
        ''' Set 1 số seri đã phát hành KHÔNG thành công vào csdl,
        để có thể phát hành lại'''
        isOk = self.order_release.UpdateOnlyReleasingNumber(order_id, no_number)
        return isOk


    # Các lệnh xuất xưởng
    def __UpdateListOrdersFactoryLocal(self, response = None) -> bool: #
        ''' Cập nhật danh sách lệnh phát hành vào local'''
        if response is None:
            return

        data_str = JsonConverter.Dumps(response, IsIgnoreNullValue = False)
        data_obj = json.loads(data_str, object_hook=lambda d: OrderFactoryModel(**d))
        for item in data_obj: # Cập nhật tất cả ds orders vào csdl
            self.order_factory.Update(item)


    def __GetSeriReleasedFactoryLocal(self, order_id:int) -> int: # 
        '''Get 1 số seri đã phát hành thành công trong csdl'''
        order : OrderFactoryModel = self.order_factory.GetOneById(order_id= order_id)
        if order is not None:
            return order.releasing_number
        else:
            return None

    def __SetSeriReleasedFactoryLocal(self, order_id:int, no_number:int) -> bool: #
        ''' Set 1 số seri đã phát hành KHÔNG thành công vào csdl,
        để có thể phát hành lại'''
        isOk = self.order_factory.UpdateOnlyReleasingNumber(order_id, no_number)
        return isOk
    #----------------------------------------------------------------- END Hàm Private -------------------------------------------------------------------------------------------


if __name__ == '__main__':
    iStampDebug.Init(debug()) # init Debug- Mỗi ứng dụng cần khởi tạo trình debug của riêng nó để có thể chạy debug ở trong thư viện

    # Khai báo và Khởi tạo 1 sealer
    SealerInfo = SealerInfo()
    SealerInfo.Device  = Device()
    SealerInfo.Username= "dqdquangdung@gmail.com"
    SealerInfo.Location= None
    SealerInfo.Token   = "free"

    # _Sealer = Sealer(SealerInfo, False)
    # ResultCheck = _Sealer.QuickCheck()
    # print('Result StampCheck:', Enum.GetName(DefCode, ResultCheck.Result))

    lib = LibHandling()
    data = lib.Login("trantrungbk95@gmail.com", "12345678")
    print(data)
    if lib.Sealer is not None:
        print("Sealer: " + lib.Sealer.Info.Username)
    else:
        print("Sealer không được khởi tạo")
    # while(True):
    #     pass

    xx = lib.GetStampBatchParameter()
    print(xx)