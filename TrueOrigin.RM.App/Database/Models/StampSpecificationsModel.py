
# Thông số kỹ thuật của cuộn tem
class StampSpecificationsModel(object):
    def __init__(self, id:int=0, name:str='', length:float= 0.0, width:float= 0.0, distance:float= 0.0, inner_diameter:float= 0.0, outer_diameter:float= 0.0):
        self.id = id
        self.name = name
        self.length = length
        self.width = width
        self.distance = distance
        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter