import sys


from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from AppDbContext import appDbContext
from OrderFactoryModel import OrderFactoryModel

class OrderFactoryRepository:
    def __init__(self):
        pass

    def GetAll(self):
        return appDbContext.OrderFactory.ToList()
    
    def GetOneById(self, order_id):
        return appDbContext.OrderFactory.FirstOrDefault('order_id', order_id)

    def Update(self, order:OrderFactoryModel): #Cập nhật Order, bỏ qua releasing_number
        return appDbContext.OrderFactory.Insert(order)

    def UpdateOnlyReleasingNumber(self, order_id, releasing_number): # chỉ cập nhật duy nhất releasing_number của Order
        order_sql : OrderFactoryModel = appDbContext.OrderFactory.FirstOrDefault('order_id', order_id)
        if order_sql is not None: # Nếu Order này đã có trong csdl, thì cập nhật tất cả, trừ releasing_number
            order_sql.releasing_number = releasing_number
        return appDbContext.OrderFactory.Insert(order_sql)


if __name__ == '__main__':  
    ss = OrderFactoryRepository()
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