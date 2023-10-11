import sys


from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from AppDbContext import appDbContext
from OrderReleaseModel import OrderReleaseModel

class OrderReleaseRepository:
    def __init__(self):
        pass

    def GetAll(self):
        return appDbContext.OrderRelease.ToList()
    
    def GetOneById(self, order_id):
        return appDbContext.OrderRelease.FirstOrDefault('order_id', order_id)

    def Update(self, order:OrderReleaseModel): #Cập nhật Order, bỏ qua releasing_number
        order_sql : OrderReleaseModel = appDbContext.OrderRelease.FirstOrDefault('order_id', order.order_id)
        if order_sql is not None: # Nếu Order này đã có trong csdl, thì cập nhật tất cả, trừ releasing_number
            order.releasing_number = order_sql.releasing_number
        return appDbContext.OrderRelease.Insert(order)

    def UpdateOnlyReleasingNumber(self, order_id, releasing_number): # chỉ cập nhật duy nhất releasing_number của Order
        order_sql : OrderReleaseModel = appDbContext.OrderRelease.FirstOrDefault('order_id', order_id)
        if order_sql is not None: # Nếu Order này đã có trong csdl, thì cập nhật tất cả, trừ releasing_number
            order_sql.releasing_number = releasing_number
        return appDbContext.OrderRelease.Insert(order_sql)


if __name__ == '__main__':  
    ss = OrderReleaseRepository()
    # result = ss.GetAll()
    # if result is not None:
    #     for item in result:
    #         print(item.__dict__)
    # else:
    #     print(None)

    result = ss.GetOneById(23)
    if result is not None:
        print(result.__dict__)
    else:
        print(None)