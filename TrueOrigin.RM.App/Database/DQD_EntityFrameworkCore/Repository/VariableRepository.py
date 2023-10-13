import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from AppDbContext import appDbContext
from VariablesModel import VariablesModel, VarProperty

class VariableRepository:
    def __init__(self):
        pass

    #Token đăng nhập
    @property
    def Token(self):
        return self.__LoadVariable('Token')
    @Token.setter
    def Token(self, value:str):
        self.__SaveVariable('Token', value)

    #Mã ngôn ngữ của ứng dụng
    @property
    def Language(self):
        return self.__LoadVariable('Language')
    @Language.setter
    def Language(self, value:str):
        self.__SaveVariable('Language', value)

    #Mã máy của ứng dụng
    @property
    def MachineId(self):
        return self.__LoadVariable('MachineId')
    @MachineId.setter
    def MachineId(self, value:str):
        self.__SaveVariable('MachineId', value)
        
    # ------------------------------------------------------------- start ĐỌC/GHI dữ liệu các biến vào SQLite -------------------------------------------------------------
    # -- ĐỌC/GHI các biến
    def __LoadVariable(self, property:str):
        var:VariablesModel = appDbContext.Variables.FirstOrDefault('property', property)
        if var is not None:
            return var.value
        else:
            return None

    def __SaveVariable(self, property:str, value:str):
        var = VariablesModel()
        var.property = property
        var.value = value
        result = appDbContext.Variables.Insert(var)
        return result
    # ------------------------------------------------------------- end ĐỌC/GHI dữ liệu các biến vào SQLite -------------------------------------------------------------

if __name__ == '__main__':  
    varRepository = VariableRepository()
    varRepository.Token = None
    print(varRepository.Token)