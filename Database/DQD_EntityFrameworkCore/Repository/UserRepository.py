import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from AppDbContext import appDbContext
from UserInfoModel import UserInfoModel

class UserRepository:
    def __init__(self):
        pass

    def GetAll(self):
        return appDbContext.InfoUser.ToList()
    
    def GetOneById(self, id):
        return appDbContext.InfoUser.FirstOrDefault('id', id)

    def Update(self, user_info):
        return appDbContext.InfoUser.Insert(user_info)

if __name__ == '__main__':  
    ss = UserRepository()
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