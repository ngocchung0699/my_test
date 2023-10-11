import inspect
import json
from math import fabs
from pathlib import Path
import sqlite3 as lite
import sys
from turtle import pu

sys.path.append(str(Path(__file__).parent.parent) + "/Models")
from StampSpecificationsModel import StampSpecificationsModel

DEBUG = False # Có debug thư viện SQLite hay ko?

class EntityFrameworkQueryable():
    conn = lite.connect(str(Path(__file__).parent.parent) + "/DQD_EntityFrameworkCore/TO_ReleaseMachine.db", check_same_thread=False)
    
    def __init__(self, Entity):
        self.Entity = Entity
        self.name_table = self.Entity.__class__.__name__.replace('Model','')

    def __Execute(self, sql_query:str):
        cur = EntityFrameworkQueryable.conn.cursor() 
        cur.execute(sql_query)

    def TableCreating(self): # Tạo bảng nếu chưa tồn tại
        attributes = [attr for attr in dir(self.Entity)  if not attr.startswith('__')]
        types = [type(getattr(self.Entity, name)).__name__ for name in dir(self.Entity) if name[:2] != '__' and name[-2:] != '__']

        # Tạo lệnh truy vấn
        # sql_create_variables = """ CREATE TABLE IF NOT EXISTS variables (name text PRIMARY KEY,interger_value interger, text_value  text); """
        sql_create = ' CREATE TABLE IF NOT EXISTS ' + self.name_table + ' ( '
        for item in attributes:  
            if item.lower() == 'id': # Nếu có trường id, thì mặc định cho nó là key chính
                sql_create += ('id INTEGER PRIMARY KEY,')
            else:
                if item == attributes[- 1]: #Nếu item cuối thì không cần thêm ','
                    sql_create += (item + ' ' + types[attributes.index(item)])
                else:
                    sql_create += (item + ' ' + types[attributes.index(item)] + ',')
        sql_create +=  ' ); '

        if DEBUG:
            print(sql_create)

        self.__Execute(sql_create)

    def ToList(self):
        '''Lấy tất cả hàng dữ liệu có trong bảng
        '''

        #SELECT distance, id, inner_diameter, length,name, outer_diameter, width FROM StampSpecifications;
        sql_tolist = 'SELECT ' 
        attributes = [attr for attr in dir(self.Entity)  if not attr.startswith('__')]
        for item in attributes:  
            if item == attributes[- 1]: #Nếu item cuối thì không cần thêm ','
                sql_tolist += (item)
            else:
                sql_tolist += (item + ',')
        sql_tolist += ' FROM ' + self.name_table

        if DEBUG:
            print(sql_tolist)

        cur = EntityFrameworkQueryable.conn.cursor()
        res = cur.execute(sql_tolist)
        rows = cur.fetchall()
        if len(rows) == 0:
            return None

        result = []
        for row in rows:
            col_names = [tup[0] for tup in res.description]
            row_values = [i for i in row]
            row_as_dict = dict(zip(col_names,row_values))

            x = json.dumps(row_as_dict)
            data = json.loads(x, object_hook=lambda d: type(self.Entity)(**d))
            result.append(data)
        return result

    def FirstOrDefault(self, where, predicate):     
        '''Tìm kiếm trong bảng 1 hàng đầu tiên có dữ liệu liên quan
        where: cột cần tìm
        predicate: thuộc tính cần tìm của cột trên
        '''
        try:
            #  cur.execute("SELECT * FROM release_orders WHERE id=? LIMIT 1", (id_ro,))
            sql_find = 'SELECT * FROM ' + self.name_table + ' WHERE ' + where + '=? LIMIT 1'
            data = (predicate,)

            if DEBUG:
                print(sql_find, data)

            cur = EntityFrameworkQueryable.conn.cursor()
            res = cur.execute(sql_find, data)
            rows = cur.fetchall()
            if len(rows) == 0:
                return None

            for row in rows:
                col_names = [tup[0] for tup in res.description]
                row_values = [i for i in row]
                row_as_dict = dict(zip(col_names,row_values))

                x = json.dumps(row_as_dict)
                return json.loads(x, object_hook=lambda d: type(self.Entity)(**d)) # Chỉ cần trả về giá trị đầu tiên tìm thấy
        except Exception as ex:
            print('[FirstOrDefault Err]: ' + str(ex))
            return None
        return None

    def Where(self, where, predicate): 
        '''Tìm kiếm trong bảng tất cả hàng dữ liệu liên quan
        where: cột cần tìm
        predicate: thuộc tính cần tìm của cột trên
        '''
        try:  
            #  cur.execute("SELECT * FROM release_orders WHERE id=? LIMIT 1", (id_ro,))
            sql_find = 'SELECT * FROM ' + self.name_table + ' WHERE ' + where + '=?'
            data = (predicate,)

            if DEBUG:
                print(sql_find, data)

            cur = EntityFrameworkQueryable.conn.cursor()
            res = cur.execute(sql_find, data)
            rows = cur.fetchall()
            if len(rows) == 0:
                return None

            result = []
            for row in rows:
                col_names = [tup[0] for tup in res.description]
                row_values = [i for i in row]
                row_as_dict = dict(zip(col_names,row_values))

                x = json.dumps(row_as_dict)
                data = json.loads(x, object_hook=lambda d: type(self.Entity)(**d))
                result.append(data)
            return result
        except Exception as ex:
            print('[Where Err]: ' + str(ex))
            return None
    
    def Update(self, where:str, predicate, entity):  
        '''Cập nhật dữ liệu trong bảng
        where: cột cần tìm
        predicate: thuộc tính cần tìm của cột trên
        entity: dữ liệu cần cập nhật
        '''
        attributes = [attr for attr in dir(entity)  if not attr.startswith('__')]

        # Tạo lệnh truy vấn
        # sql = """Update release_orders set + = ?, status = ?  where id = ?"""
        sql_update ='UPDATE ' + self.name_table + ' SET '
        for item in attributes:
            if item == attributes[- 1]:
                sql_update += (item + ' = ? ')
            else:
                sql_update += (item + ' = ?, ')
        sql_update +=  'WHERE ' + where + ' = ' + str(predicate)

        #Chuyển dữ liệu của class sang tuple
        arr = []
        for item in attributes:
            arr.append(vars(entity)[item])
        data = tuple(arr)

        if DEBUG:
            print(sql_update, data)

        cur = EntityFrameworkQueryable.conn.cursor()
        cur.execute(sql_update, data)
        EntityFrameworkQueryable.conn.commit()
        if cur.rowcount < 1:  #error
            return False
        else: #success
            return True

    def Insert(self, entity):  
        '''Thêm mới hoặc sửa 1 hàng dữ liệu của 1 bảng nếu Key chính trùng nhau
        - Nếu entity có id. thì cố gắng tìm id đó để sửa. còn entity không có id( default = 0) thì thêm mới 
        entity: dữ liệu cần thêm mới
        '''
        # self.FirstOrDefault(entity)
        attributes = [attr for attr in dir(entity)  if not attr.startswith('__')]
        # Tạo lệnh truy vấn
        #  sql = ''' INSERT INTO stamps(number_cur,serinumber,time,status,id_release_order) VALUES(?,?,?,?,?) '''
        sql_insert ='INSERT OR REPLACE INTO ' + self.name_table + ' ( '
        for item in attributes:
            if item.lower() != 'id' or vars(entity)[item] != 0: # Nếu có trường id, thì mặc định cho nó là key chính, nên bỏ qua
                if item == attributes[- 1]:
                    sql_insert += (item + ' ) ')
                else:
                    sql_insert += (item + ', ')
            
        sql_insert +=  'VALUES ( '

        for item in attributes:
            if item.lower() != 'id' or vars(entity)[item] != 0: # Nếu có trường id, thì mặc định cho nó là key chính, nên bỏ qua
                if item == attributes[- 1]:
                    sql_insert += '?)'
                else:
                    sql_insert += '?,'

        #Chuyển dữ liệu của class sang tuple
        arr = []
        for item in attributes:
            if item.lower() != 'id' or vars(entity)[item] != 0: # Nếu có trường id, thì mặc định cho nó là key chính, nên bỏ qua
                arr.append(vars(entity)[item])
        data = tuple(arr)

        if DEBUG:
            print(sql_insert, data)

        cur = EntityFrameworkQueryable.conn.cursor()
        cur.execute(sql_insert, data)
        EntityFrameworkQueryable.conn.commit()
        if cur.rowcount < 1:  #error
            return False
        else: #success
            return True

if __name__ == '__main__':  
    Entity = EntityFrameworkQueryable(StampSpecificationsModel())
    Entity.TableCreating()
    # value = Entity.FirstOrDefault('distance', 'distance')
    # print(value.width)

    dqd = StampSpecificationsModel()
    dqd.name = 'ntag 213 NXP xxx'
    dqd.id = 30
    dqd.distance = 1.2
    dqd.inner_diameter = 1.1
    dqd.outer_diameter = 5.5
    # value = Entity.Update(where='id', predicate=dqd.id, entity= dqd)
    # print(value)

    value = Entity.Insert(entity= dqd)
    print(value)
    # print(tuple(dqd.__dict__))
    # varrr = Variables(property=15, value= "DQD")
    # attributes = [attr for attr in dir(varrr)  if not attr.startswith('__')]
   

    # l = []
    # for item in attributes:
    #     print(vars(varrr)[item])
    #     l.append(vars(varrr)[item])
    # print(tuple(l))