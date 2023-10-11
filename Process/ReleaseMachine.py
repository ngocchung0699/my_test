from PyQt5 import QtCore, QtGui, QtWidgets
from Database.DQD_EntityFrameworkCore.Repository.VariableRepository import VariableRepository
from Views.ViewHandling import ViewHandling
import enumerate.enum_init as enum
from Libraries.LibHandling import LibHandling, ResultLogin, MachineFunc
                
class ReleaseMachine(ViewHandling):
    def __init__(self, ui, lang):
        super().__init__()
        self.Library = LibHandling()
        self.ui = ui 
        self.lang = lang
        self.variableRepository = VariableRepository()

        self.statusRO           = []
        self.statusRO.clear()
        self.statusRO.append(lang['status_ro']['APPROVING'])
        self.statusRO.append(lang['status_ro']['DISABLE'])
        self.statusRO.append(lang['status_ro']['READY'])
        self.statusRO.append(lang['status_ro']['RELEASING'])
        self.statusRO.append(lang['status_ro']['COMPLETE'])
        self.statusRO.append(lang['status_ro']['STOP'])
        self.statusRO.append(lang['status_ro']['PAUSE'])

    def get_order(self):
        self.get_ro_server()    # Lấy dah sách lệnh phát hành
        self.dump_data_table_ro() # hiển thị ds vào list view
        return self.list_ro

    #Lấy tất cả Lệnh phát hành của account
    def get_ro_server(self):
        try:
            result = self.Library.GetAllOrders()
            if result is not None:
                print('List orders Release: ', result.Count)
                self.list_ro = result
            else:
                print('List orders Release is Null')
                self.list_ro = []
    
            # self.ui.table_releaser_order_2.setRowCount(0)
        except:
            self.status_bar_mess = enum.sBar.ERROR_SERVER

            self.list_ro = []

    def dump_data_table_ro(self):
        self.ui.table_releaser_order.setRowCount(0) # Clear table
        for item in self.list_ro:
            row = self.ui.table_releaser_order.rowCount()
            self.ui.table_releaser_order.setRowCount(row + 1)
            self.ui.table_releaser_order.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item.order_id)))
            self.ui.table_releaser_order.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item.total_seri)))
            self.ui.table_releaser_order.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item.start_seri)))
            self.ui.table_releaser_order.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item.no_number)))

            # update
            if int(item.status) == enum.sRO.RELEASING.value or int(item.status) == enum.sRO.PAUSE.value:
                if int(item.status) == enum.sRO.PAUSE.value:
                    self.ui.table_releaser_order.setItem(row, 4, QtWidgets.QTableWidgetItem(str(self.statusRO[enum.sRO.PAUSE.value])))
                    self.ui.table_releaser_order.item(row, 4).setForeground((QtGui.QColor(255, 210, 51)))
                else:
                    self.ui.table_releaser_order.setItem(row, 4, QtWidgets.QTableWidgetItem(str(self.statusRO[enum.sRO.RELEASING.value])))
                    self.ui.table_releaser_order.item(row, 4).setForeground((QtGui.QColor(0, 114, 173)))

            else:
                self.ui.table_releaser_order.setItem(row, 4, QtWidgets.QTableWidgetItem(str(self.statusRO[int(item.status)])))
                if int(item.status) == enum.sRO.READY.value:
                    self.ui.table_releaser_order.item(row, 4).setForeground((QtGui.QColor(25, 221, 115)))
                else:
                    self.ui.table_releaser_order.item(row, 4).setForeground((QtGui.QColor(100, 24, 195)))