class UserInfoModel(object):
    def __init__(self, id:int=0, name:str='', email:str='', sex:str='', birthday:str='', phone_num:str='', picture:str='', ByteArray_img= None, username:str='', password:str='',
        c_password:str='', location=None, mac_address:str='', company:str='', url_company:str='',description:str='',address:str='',provider:str='',token:str='', token_fcm:str='',
        facility_vi:str='', facility_en:str=''):
        self.id = id
        self.name = name
        self.email = email
        self.sex = sex
        self.birthday = birthday
        self.phone_num = phone_num
        self.picture = picture
        self.ByteArray_img = ByteArray_img
        self.username = username
        self.password = password
        self.c_password = c_password
        self.location = location
        self.mac_address = mac_address
        self.company = company
        self.url_company = url_company
        self.description = description
        self.address = address
        self.provider = provider
        self.token = token
        self.facility_vi = facility_vi
        self.facility_en = facility_en
        self.token_fcm = token_fcm
