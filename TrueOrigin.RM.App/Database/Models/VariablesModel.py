from enum import Enum


class VarProperty(Enum):
    Token = 'token'

# Các biến lưu riêng lẻ
class VariablesModel(object):
    def __init__(self, property:VarProperty= '', value:any= ''):
        self.property = property
        self.value = value
