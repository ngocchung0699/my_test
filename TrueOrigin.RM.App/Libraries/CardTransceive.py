from CardNFC.pn532.pn532 import *
from CardNFC.pn532.spi import PN532_SPI

from hashlib import sha256

_NUM_TRY        = 1

#NTAG213
AUTH0_213   = 0x29
PWD_213     = 0x2B
PACK_213    = 0x2C
PROT_213    = 0x2A
AUTHLIM_213 = 0x2A  

#NTAG215
AUTH0_215   = 0x83
PWD_215     = 0x85
PACK_215    = 0X86
PROT_215    = 0X84
AUTHLIM_215 = 0X84  

#NTAG216
AUTH0_216   = 0xE3
PWD_216     = 0xE5
PACK_216    = 0XE6
PROT_216    = 0XE4
AUTHLIM_216 = 0XE4  

STORAGE_SIZE_213    = 0x0F
STORAGE_SIZE_215    = 0x11
STORAGE_SIZE_216    = 0x13

STORAGE_INDEX       = 0x07
PWD_AUTH            = 0x1b

class CardTransceive():
    def __init__(self):
        super().__init__()
        self.pn532 = PN532_SPI(debug=False, reset=20, cs=4) 

        try:
            ic, ver, rev, support = self.pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
            self.pn532.SAM_configuration()
        except:
            pass
    
        self.auth0_stamp = None
        self.pwd_stamp = None
        self.pack_stamp = None
        self.prot_stamp = None
        self.authlim_stamp = None

    def Transceive(self, params = [0x60]):
        try:
            len_data = len(params)
            # Get version
            if len_data == 1:
                response_len = 9
            # Read data
            elif len_data == 2:
                response_len = 17
            # Read auth
            elif len_data == 5:
                response_len = 3
            # Write data
            elif len_data == 6:
                response_len = 1
            else:
                return None

            response = self.pn532.call_function( params=params, response_length=response_len)
            # print('Transceive NFC response: ', response)
            if(len(response) <= 1): # Đây là lỗi trả về
                self.TryConnect() # Nếu lỗi thử tryConnect lại thẻ để thực hiện lệnh tiếp theo
            return response[1:]
        except:
            # print('except Trans NFC')
            self.TryConnect() # Nếu lỗi thử tryConnect lại thẻ để thực hiện lệnh tiếp theo
            return None

    def Read_page(self, index):
        return self.Transceive(params=[MIFARE_CMD_READ, index])
    
    def Write_page(self, block_number, data):
        params = bytearray(2+len(data))
        params[0] = MIFARE_ULTRALIGHT_CMD_WRITE
        params[1] = (block_number) & 0xFF
        params[2:] = data
        return self.Transceive(params=params)
    
    def Write_data_init_stamp(self, id, version = 0x03):
        data_id1 = id[0:4]
        data_id2 = id[4:]
        self.Write_page(4, data_id1)
        self.Write_page(5, data_id2)

        for x in range(6, 27):
            data = bytes([0x00, 0x00, 0x00, 0x00])
            if self.Write_page(x, data) is None:
                return False
        data_version = bytes([version, 0x00, 0x00, 0x00])
        self.Write_page(39, data_version)
        return True

    def write_authenticate(self, pwd):
        data_auth = pwd[0:4]
        self.Write_page(38, data_auth)
        return True

    def TryConnect(self):
        try:
            for x in range(_NUM_TRY):
                uid = self.pn532.read_passive_target(timeout=0.1)
                if uid is not None:
                    uid_int = int.from_bytes(uid[0:8], byteorder='little', signed=True)
                    # print('------Found card: ', uid)
                    return uid_int
            return False
        except:
            return False
    
    def GetInfoTag(self):
        try:
            response = self.Transceive(params = [0x60])
            if response:
                # #print('Read frame: ', [hex(i) for i in response])
                if hex(response[STORAGE_INDEX]) == hex(STORAGE_SIZE_213):
                    self.auth0_stamp = AUTH0_213
                    self.pwd_stamp = PWD_213
                    self.pack_stamp = PACK_213
                    self.prot_stamp = PROT_213
                    self.authlim_stamp = AUTHLIM_213
                elif hex(response[STORAGE_INDEX]) == hex(STORAGE_SIZE_215):
                    self.auth0_stamp = AUTH0_215
                    self.pwd_stamp = PWD_215
                    self.pack_stamp = PACK_215
                    self.prot_stamp = PROT_215
                    self.authlim_stamp = AUTHLIM_215
                elif hex(response[STORAGE_INDEX]) == hex(STORAGE_SIZE_216):
                    self.auth0_stamp = AUTH0_216
                    self.pwd_stamp = PWD_216
                    self.pack_stamp = PACK_216
                    self.prot_stamp = PROT_216
                    self.authlim_stamp = AUTHLIM_216
                else:
                    return False
                return True
            else:
                #print('None ')
                return False
        except :
            return False

    def CreatePwd(self):
        try:
            response = self.Transceive(params = [0x30, 0])
            if response:
                uid = response[1:9]
                # print(uid)
                str_uid = ''.join(str(format(e, '02x')) for e in uid)
                uid_hash = sha256(bytes.fromhex(str_uid)).digest()
                #print('Read onpensecu2: ', [hex(i) for i in uid_hash])
                pwd = [uid_hash[2], uid_hash[0], uid_hash[1], uid_hash[5], uid_hash[0], uid_hash[3]]
                #print('Read CreatePwd: ', [hex(i) for i in pwd])
                return pwd
            else :
                return False
        except :
            return False

    def OpenSecurity(self, pwd):
        try:
            params = [PWD_AUTH] + pwd[0:4]
            #print('OpenSecurity params: ', [hex(i) for i in params])
            response = self.Transceive(params = params)
            if response:
                #print('Read onpensecu1: ', [hex(i) for i in response])
                for i, item in enumerate(response[1:]):
                    if hex(pwd[i + 4]) != hex(item):
                        return False
                response2 = self.Transceive(params = [MIFARE_CMD_READ, self.auth0_stamp])
                #print('Read onpensecu2: ', [hex(i) for i in response2])
                if response2:
                    params3 = [MIFARE_ULTRALIGHT_CMD_WRITE, self.auth0_stamp, response2[1] , response2[2], response2[3], 0xff]
                    #print('Read onpensecu3: ', [hex(i) for i in params3])
                    response3 = self.Transceive(params = params3)
                    # print(response3)
                    return response3
            return False
        except :
            return False

    def CloseSecurity(self):
        try:
            # params3 = [MIFARE_ULTRALIGHT_CMD_WRITE, 0x06, 0x01 , 0x02, 0x03, 0x04 ]
            # response3 = self.Transceive(params = params3)
            # #print('Read response3: ', [hex(i) for i in response3])
            response = self.Transceive(params = [MIFARE_CMD_READ, self.auth0_stamp])
            # #print('Read response: ', [hex(i) for i in response])
            start_index = 1
            if response:
                params3 = [MIFARE_ULTRALIGHT_CMD_WRITE, self.auth0_stamp, response[start_index + 0] , response[start_index + 1], response[start_index + 2], 0x02]
                response3 = self.Transceive(params = params3)
                # print(response3)
                # #print('Read response3: ', [hex(i) for i in response3])
                return response3
            return False
        except :
            return False

    def IsProtectedPwd(self):
        try:
            response = self.Transceive(params = [MIFARE_CMD_READ, self.auth0_stamp])
            # #print('Read IsProtectedPwd', [hex(i) for i in response])
            if response:
                if hex(response[4]) ==  hex(0xFF):
                    return False
            return True
        except :
            return True

    def SetPwd(self, pwd):
        # 1. Đặt PWD (trang 43) thành mật khẩu mong muốn của bạn (giá trị mặc định là 0xFFFFFFFF).
        params1 = [MIFARE_ULTRALIGHT_CMD_WRITE, self.pwd_stamp] + pwd[0:4]
        result1 = self.Transceive(params=params1)
        # print('SetPwd 1 ----------------------------')
        # print('Read params1', [hex(i) for i in params1])
        # print('Read result1: ', [hex(i) for i in result1])
        
        # 2. Đặt PACK (trang 44, byte 0-1) thành xác nhận mật khẩu mong muốn của bạn (giá trị mặc định
        params2 = [MIFARE_ULTRALIGHT_CMD_WRITE, self.pack_stamp, pwd[4], pwd[5], 0, 0]
        result2 = self.Transceive(params=params2)
        # print('SetPwd 2 ----------------------------')
        # print('Read params2', [hex(i) for i in params2])
        # print('Read result2: ', [hex(i) for i in result2])

        # 3. Đặt AUTHLIM (trang 42, byte 0, bit 2-0) thành số lần thử xác minh mật khẩu không thành công tối đa (đặt giá trị này thành 0 sẽ cho phép số lần thử PWD_AUTH không giới hạn).

        # 4. Đặt PROT (trang 42, byte 0, bit 7) thành giá trị mong muốn (0 = PWD_AUTH chỉ cần cho truy cập ghi, 1 = PWD_AUTH cần thiết cho truy cập đọc và ghi).
        result3 = self.Transceive(params=[MIFARE_CMD_READ, self.prot_stamp])
        # print('SetPwd 3 ----------------------------')
        # print('Read result3: ', [hex(i) for i in result3])
        if result3 and len(result3)>4:
            val_prot = True
            val_authlim = 0 
            data_prot = 0x80 if val_prot == True else 0x00
            params4 = [MIFARE_ULTRALIGHT_CMD_WRITE, self.prot_stamp, ((result3[1] & 0x78) | (data_prot) | (val_authlim & 0x07)), result3[2], result3[3], result3[4]]
            result4 =self.Transceive(params=params4)
            # print('SetPwd 4 ----------------------------')
            # print('Read params4', [hex(i) for i in params4])
            # print('Read result4', [hex(i) for i in result4])
            
        # 5. Đặt AUTH0 (trang 41, byte 3) thành trang đầu tiên yêu cầu xác thực mật khẩu.
        return self.CloseSecurity()


    def ReleaseStamp(self, seri_stamp):
        '''Đang mặc định phát hành 1 phiên bản tem duy nhất v0003'''
        bytes_seri = seri_stamp.to_bytes(8, 'little')
        if self.TryConnect():
            if self.GetInfoTag():
                pwd = self.CreatePwd()
                if pwd:
                    if self.IsProtectedPwd(): 
                        if self.TryConnect():  
                            if self.OpenSecurity(pwd):
                                if self.Write_data_init_stamp(bytes_seri) and self.write_authenticate(pwd):
                                    if self.SetPwd(pwd):
                                        return True
                            else:
                                # print('NFC Open Security Err')
                                return False
                    else:
                        if self.Write_data_init_stamp(bytes_seri) and self.write_authenticate(pwd):
                            if self.SetPwd(pwd):
                                return True
                else:
                    print('NFC Create pwd err')
            else:
                print('NFC Get info err')
        else:
            print('NFC Connect Err')
        return False

    def ReadIdCard(self):
        if self.GetInfoTag():
            pwd = self.CreatePwd()
            if pwd != False:
                if self.OpenSecurity(pwd):
                    page4 = self.Read_page(4)
                    self.CloseSecurity()
            
                    if page4 != False and page4 != None and len(page4) >8:
                        try:
                            ID_card = int.from_bytes(page4[1:9], byteorder='little', signed=True)
                            # print('Read NFC OK %s', ID_card)
                            return ID_card
                        except IOError as e:
                            # print('NFC: Error occurred ' + str(e))
                            return None
                    else:
                        return None
                else:
                    # print('OpenSecurity NFC Err')
                    return None
            else:
                # print('CreatePwd NFC Err')
                return None
        else:
            # print('GettagInfo NFC Err')
            return None