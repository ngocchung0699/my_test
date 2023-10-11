from pathlib import Path
import sys
from typing import List

sys.path.append("Database/DQD_EntityFrameworkCore")
from DbSet import DbSet

sys.path.append("Database/Models")
from StampSpecificationsModel import StampSpecificationsModel
from OrderReleaseModel import OrderReleaseModel
from OrderFactoryModel import OrderFactoryModel
from VariablesModel import VariablesModel
from UserInfoModel import UserInfoModel

class AppDbContext:
    def __init__(self):
        #Khởi tạo dữ liệu
        self.StampSpecifications = DbSet(StampSpecificationsModel())
        self.OrderRelease = DbSet(OrderReleaseModel())
        self.OrderFactory = DbSet(OrderFactoryModel())
        self.Variables = DbSet(VariablesModel())
        self.InfoUser = DbSet(UserInfoModel())

        #Tạo bảng dữ liệu trong SqlLite nếu chưa có
        self.OnModelCreating()

    def OnModelCreating(self): # Tạo bảng nếu chưa có
        self.StampSpecifications.TableCreating()
        self.OrderRelease.TableCreating()
        self.OrderFactory.TableCreating()
        self.Variables.TableCreating()
        self.InfoUser.TableCreating()

appDbContext = AppDbContext()

if __name__ == '__main__':  
    stamp_spec: List[StampSpecificationsModel]  = appDbContext.StampSpecifications.Where('distance', 'distance')
    if stamp_spec is not None:
        print(stamp_spec[1].width)
    else:
        print('stamp_spec is null')

    order : OrderReleaseModel= appDbContext.OrderReleaseModel.FirstOrDefault('order_id', 'order_id')
    if order is not None:
        print(order.__dict__)
    else:
        print('order is null')