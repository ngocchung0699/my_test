from enum import Enum
from pathlib import Path
import sqlite3 as lite
from sqlite3 import Error

from StampSpecificationsModel import StampSpecificationsModel
from VariablesModel import VariablesModel

class Tables_TrueOriginRM_db(Enum):
    stamp_specifications        = "stamp_specifications"
    variables                   = "variables"

class TrueOriginRM_db() :
    def __init__(self):
        super().__init__()
        self.conn = None
        self.StampSpecifications = StampSpecificationsModel()
        self.Variables = VariablesModel()

    def select_ro_local(self, id_ro):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM release_orders WHERE id=? LIMIT 1", (id_ro,))
        rows = cur.fetchall()
        for row in rows:
            return row
        return None

    def select_stamps_local(self, id_ro):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM stamps WHERE id_release_order=?", (id_ro,))
        rows = cur.fetchall()
        return rows

    def select_number_cur_max(self, id_ro):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM stamps WHERE id_release_order=? ORDER BY number_cur DESC LIMIT 1", (id_ro,))
        rows = cur.fetchall()
        for row in rows:
            return (int(row[1]))

    def select_current_seri_local(self, id_ro):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM release_orders WHERE id=? ORDER BY current_seri DESC LIMIT 1", (id_ro,))
        rows = cur.fetchall()
        for row in rows:
            return (int(row[7]))

    def select_seri_cur(self, id_batch):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM stamps WHERE id_batch=? ORDER BY time DESC LIMIT 1", (id_batch,))
        rows = cur.fetchall()
        for row in rows:
            return (int(row[1]) + 1)

    # Lấy biến
    def select_variables(self, variable):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM variables WHERE name=? LIMIT 1", (variable,))
        rows = cur.fetchall()
        for row in rows:
            return row

    def insert_ro_local(self, ro_item):
        sql = ''' insert or replace into release_orders(id,id_user,id_batch,id_producer,id_product,total_seri,start_seri,current_seri,status,time)
                VALUES(?,?,?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, ro_item)
        self.conn.commit()
        return cur.lastrowid

    # lưu biến
    def insert_variable(self, name,  value = None):
        sql = ''' insert or replace into variables(property,value) VALUES(?,?) '''
        cur = self.conn.cursor()
        data = [name, value]
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid

    def insert_stamp(self, stamp):
        sql = ''' INSERT INTO stamps(number_cur,serinumber,time,status,id_release_order)
                VALUES(?,?,?,?,?) '''

        cur = self.conn.cursor()
        cur.execute(sql, stamp)
        self.conn.commit()
        return cur.lastrowid

    def update_ro_local(self, id_ro, current_seri, status = None):
        # time = QDateTime.currentDateTime()
        # timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss')
        if status is None:
            sql = """Update release_orders set current_seri = ?  where id = ?"""
            data = (current_seri, id_ro)
        else:
            sql = """Update release_orders set current_seri = ?, status = ?  where id = ?"""
            data = (current_seri, status, id_ro)

        cur = self.conn.cursor()
        cur.execute(sql, data)
        self.conn.commit()

    def create_connection(self, path: str):
        try:
            self.conn = lite.connect(path)
        except Error as e:
            print(e)

class SQLiteHandling():
    def __init__(self):
        super().__init__()
        self.conn = lite.connect(str(Path(__file__).parent.parent) + "/SqlLite/trueorigin_rm.db")

    #Token đăng nhập
    @property
    def Token(self):
        return self.__LoadVariable('Token')
    @Token.setter
    def Token(self, value:str):
        self.__SaveVariable('Token', value)

    #thông tin tài khoản đăng nhập
    @property
    def InfoUser(self):
        return self.__LoadVariable('InfoUser')
    @InfoUser.setter
    def InfoUser(self, value:str):
        self.__SaveVariable('InfoUser', value)

    #thông tin lệnh phát hành
    @property
    def ReleaseOrders(self):
        return self.__LoadVariable('ReleaseOrders')
    @ReleaseOrders.setter
    def ReleaseOrders(self, value:str):
        self.__SaveVariable('ReleaseOrders', value)

    #thông số kỹ thuật của cuộn tem đang sử dụng
    @property
    def StampSpecifications(self):
        return self.__LoadVariable('StampSpecifications')
    @StampSpecifications.setter
    def ReleaseOrders(self, value:str):
        self.__SaveVariable('StampSpecifications', value)

    # ------------------------------------------------------------- start ĐỌC/GHI dữ liệu vào local -------------------------------------------------------------
    # -- ĐỌC/GHI các biến
    def __LoadVariable(self, property:str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM variables WHERE property=? LIMIT 1", (property,))
        rows = cur.fetchall()
        for row in rows:
            return row[row.index(property) + 1]

    def __SaveVariable(self, property:str, value:str):
        sql = ''' insert or replace into variables(property,value) VALUES(?,?) '''
        cur = self.conn.cursor()
        data = [property, value]
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid
    # ------------------------------------------------------------- end ĐỌC/GHI dữ liệu vào local -------------------------------------------------------------


if __name__ == '__main__':  
    db = SQLiteHandling()
    # db.Token = "DQD"
    print(db.Token)
