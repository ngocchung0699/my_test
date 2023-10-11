from PyQt5 import QtCore, QtGui, QtWidgets
from Database.DQD_EntityFrameworkCore.Repository.VariableRepository import VariableRepository
from Views.ViewHandling import ViewHandling
import enumerate.enum_init as enum
from Libraries.LibHandling import LibHandling, ResultLogin, MachineFunc

class FormattingMachine(ViewHandling):
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

        self.ui.table_releaser_order_2.itemClicked.connect(self.slot_table_format_order) # Event click 1 item trong bảng danh sách lệnh xuất xưởng lấy từ server

    def get_order(self):
        self.get_ro_server()    # Lấy dah sách lệnh xuất xưởng
        self.dump_data_table_ro() # hiển thị ds vào list view
        return self.list_ro

    #Lấy tất cả Lệnh xuất xưởng của account
    def get_ro_server(self):
        try:
            result = self.Library.GetAllOrdersFactory()
            if result is not None:
                print('List orders Factory: ', result.Count)
                self.list_ro = result
            else:
                print('List orders is Null')
                self.list_ro = []
    
            # self.ui.table_releaser_order_2.setRowCount(0)
        except:
            self.status_bar_mess = enum.sBar.ERROR_SERVER

            self.list_ro = []

    def dump_data_table_ro(self):
        self.ui.table_releaser_order_2.setRowCount(0) # Clear table
        if self.list_ro is not None:
            for item in self.list_ro:
                row = self.ui.table_releaser_order_2.rowCount()
                self.ui.table_releaser_order_2.setRowCount(row + 1)
                self.ui.table_releaser_order_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item.order_id)))
                self.ui.table_releaser_order_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item.total_number)))
                self.ui.table_releaser_order_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item.no_number)))

                # update
                if int(item.status) == enum.sRO.RELEASING.value or int(item.status) == enum.sRO.PAUSE.value:
                    if int(item.status) == enum.sRO.PAUSE.value:
                        self.ui.table_releaser_order_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.statusRO[enum.sRO.PAUSE.value])))
                        self.ui.table_releaser_order_2.item(row, 3).setForeground((QtGui.QColor(255, 210, 51)))
                    else:
                        self.ui.table_releaser_order_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.statusRO[enum.sRO.RELEASING.value])))
                        self.ui.table_releaser_order_2.item(row, 3).setForeground((QtGui.QColor(0, 114, 173)))

                else:
                    self.ui.table_releaser_order_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.statusRO[int(item.status)])))
                    if int(item.status) == enum.sRO.READY.value:
                        self.ui.table_releaser_order_2.item(row, 3).setForeground((QtGui.QColor(25, 221, 115)))
                    else:
                        self.ui.table_releaser_order_2.item(row, 3).setForeground((QtGui.QColor(100, 24, 195)))

    def slot_table_format_order(self):
        # Enable btn chọn order
        self.button_setEnable(self.ui.btn_format_select, True)
        # self.button_setEnable(self.ui.btn_repair_ro, True) # tạm thời chưa có chức năng sửa lệnh phát hành trực tiếp trên máy phát hành

        r = self.ui.table_releaser_order_2.currentRow()
        id = self.ui.table_releaser_order_2.item(r,0).text()
        self.ui.label.setText(self.lang['gui']['label'] + str(id))

        for item in self.list_ro:
            if str(item.order_id) == str(id):
                producer_name = str(item.facility_name)
                id = str(item.order_id)
                total = str(item.total_number)
                current = str(item.no_number)
                status = int(item.status)
                
                if status == enum.sRO.READY.value or status == enum.sRO.PAUSE.value or status == enum.sRO.RELEASING.value:
                    self.button_setEnable(self.ui.btn_format_select, True)
                else:
                    self.button_setEnable(self.ui.btn_format_select, False)
                    
                self.ui.rtb_detail_ro_2.clear()
                self.ui.rtb_detail_ro_2.append(self.lang['btn_select']['PRODUCER'] + producer_name)
                # self.ui.rtb_detail_ro_2.append(self.lang['btn_select']['PRODUCE_ID'] + product_id)
                self.ui.rtb_detail_ro_2.append(self.lang['btn_select']['PRODUCTION_ID'] + id)
                self.ui.rtb_detail_ro_2.append(self.lang['btn_select']['TOTAL_SERI'] + total)
                self.ui.rtb_detail_ro_2.append(self.lang['btn_select']['CURRENT_SERI'] + current)
                self.ui.rtb_detail_ro_2.append(self.lang['btn_select']['STATUS'] + str(self.statusRO[status]))
