from pickletools import uint2, uint8

from OrderReleaseModel import OrderStatus

class OrderFactoryModel(object):
    def __init__(self, order_id:int= 0, order_name:str= '', batch_name:str= '', facility_name:str= '', total_number:uint2= 0, no_number:uint2= 0, status:OrderStatus= 0,):
        self.order_id = order_id
        self.order_name = order_name
        self.batch_name = batch_name
        self.facility_name = facility_name
        self.total_number = total_number
        self.no_number = no_number
        self.status = status
