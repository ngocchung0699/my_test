from enum import Enum
import json
from pickletools import uint2, uint8

class OrderStatus(Enum):
    Approving   = 0
    Disable     = 1
    Ready       = 2
    Releasing   = 3
    Complete    = 4
    Stop        = 5
    Pause       = 6

class ProductType(Enum):
    ProductNormal_Seal5 = 1001   #sản phẩm hàng hóa bình thường 5 tâng bảo mật
    ProductNormal_Seal3 = 1002   #sản phẩm hàng hóa bình thường 3 tâng bảo mật
    NameCard_Seal5      = 2001   #thẻ nhân viên, thành viên,... 5 tâng bảo mật
    NameCard_Seal3      = 2002   #thẻ nhân viên, thành viên,... 3 tâng bảo mật

class OrderReleaseModel(object):
    def __init__(self, order_id:int= 0, order_name:str= '', batch_name:str= '', product_name:str= '', facility_name:str= '', start_seri:uint8= 0, total_seri:uint2= 0, no_number:uint2= 0, releasing_number:uint8= None,  status:OrderStatus= 0, product_type:ProductType= 0):
        self.order_id = order_id
        self.order_name = order_name
        self.batch_name = batch_name
        self.product_name = product_name
        self.facility_name = facility_name
        self.start_seri = start_seri
        self.total_seri = total_seri
        self.no_number = no_number
        self.releasing_number = releasing_number
        self.status = status
        self.product_type = product_type



def convert(data) ->OrderReleaseModel:
    #Có 2 cách để get json sang class
    return json.loads(json.dumps(data), object_hook=lambda d: OrderReleaseModel(**d))

    # j = json.loads(json.dumps(data))
    # return OrderReleaseModel(**j)

if __name__ == '__main__':
    data = {
        "order_id": 6,
        "order_name": "2",
        "batch_name": "THẦN TÀI MAY MẮN SBJ LOẠI 1.0 CHỈ",
        "product_name": "THẦN TÀI MAY MẮN SBJ LOẠI 1.0 CHỈ",
        "facility_name": "CÔNG TY TNHH MỘT THÀNH VIÊN VÀNG BẠC ĐÁ QUÝ NGÂN HÀNG SÀI GÒN THƯƠNG TÍN",
        "start_seri": 1225542052893231556,
        "total_seri": 2500,
        "no_number": 0,
        "status": 2,
        "product_type": 1001
    }

    result = convert(data)
    print(ProductType(result.product_type).name)
    pass
