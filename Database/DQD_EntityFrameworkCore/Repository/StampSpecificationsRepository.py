import sys


from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from AppDbContext import appDbContext
from StampSpecificationsModel import StampSpecificationsModel

class StampSpecificationsRepository:
    def __init__(self):
        pass

    def GetAll(self):
        '''lấy tất cả thông số kỹ thuật trong csdl'''
        return appDbContext.StampSpecifications.ToList()
    
    def GetOneById(self, id):
        '''lấy 1 thông số kỹ thuật tem theo id'''
        return appDbContext.StampSpecifications.FirstOrDefault('id', id)

    def Update(self, spec:StampSpecificationsModel): 
        '''Cập nhật 1 thông số kỹ thuật của tem'''
        return appDbContext.StampSpecifications.Insert(spec)

if __name__ == '__main__':  
    ss = StampSpecificationsRepository()
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