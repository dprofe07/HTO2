from PyQt5 import QtCore, QtGui, QtWidgets
from toolz import *
from order_unit import *


class OrderDialog(object):
    def __init__(self, parent, conn, row=None):
        super().__init__()
        self.parent = parent
        self.conn = conn
        self.row = row
        if self.row is None:
            max_id = conn.execute('select max(id) from orders').fetchone()[0]
            self.idx = 1 if max_id is None else max_id + 1
        else:
            self.idx = get_id_by_row(conn, 'orders', row, False)

    def cancel(self):
        if self.row is None:
            self.delete_all_units()

    def submit(self):
        client_id = self.comboBox.currentIndex()
        client_id = get_id_by_row(self.conn, 'clients', client_id, False)
        payment_type = self.comboBox_2.currentText()
        total = self.doubleSpinBox.value()

        if self.tableWidget.rowCount() == 0:
            return error('Нельзя оформить пустой заказ!')
        
        if self.edit:
            self.conn.execute(f'''update orders set client_id={client_id},
                payment_type="{payment_type}", total={total} where id={self.idx}''')
            self.conn.commit()
            self.parent.update_at_row('orders', self.row)
        else:
            self.conn.execute(f'''insert into orders(id, payment_type, client_id, total) 
                values({self.idx}, "{payment_type}", {client_id}, {total})''')
            self.conn.commit()
            self.parent.add_last('orders')
            self.row = 0
        self.win.close()

    def prepare(self):
        if self.row is not None:
            self.edit = True
            data = self.conn.execute(self.parent.content_request('orders', idx=self.idx)).fetchone()
            self.comboBox.setCurrentText(data[0])
            self.comboBox_2.setCurrentText(data[1])
        else:
            self.edit = False

    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(650, 367)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 631, 71))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 241, 17))
        self.label_3.setObjectName("label_3")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 120, 631, 161))
        self.tableWidget.setObjectName("tableWidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 290, 631, 27))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 330, 631, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setHorizontalSpacing(10)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.horizontalLayoutWidget_2)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setMinimum(0)
        self.doubleSpinBox.setMaximum(1_000_000)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.prepare()

        self.pushButton.clicked.connect(self.submit)
        self.pushButton_5.clicked.connect(self.create_unit)
        self.pushButton_4.clicked.connect(self.edit_unit)
        self.pushButton_3.clicked.connect(self.delete_unit)
        all_clients = [name[0] for name in self.conn.execute('''
            select name from clients
        ''').fetchall()]
        self.comboBox.addItems(all_clients)
        self.comboBox_2.addItems([
            'Кредит', 'Предоплата'
        ])
        self.tableWidget.setColumnCount(3)
        self.set_headers(self.tableWidget, ['Тур', 'Итого (руб)', 'Кол-во человек'])
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.doubleClicked.connect(self.dbclick)
        self.update_all()
        MainWindow.closeEvent = lambda x: self.cancel()
        self.pushButton_2.clicked.connect(MainWindow.close)


    def dbclick(self):
        self.edit_unit()

    def set_headers(self, table, cols):
        table.setHorizontalHeaderLabels(cols)
        table.setColumnWidth(0, 230)
        table.setColumnWidth(1, 180)
        table.setColumnWidth(2, 180)
            

    def fill_order_units(self):
        content = self.conn.execute('''
            select h.name, price, people, total from order_units as ou join tours as t on
            t.id = ou.tour_id join hotels as h on t.hotel_id = h.id
        ''').fetchall()
        print(content)


    def get_total(self):
        prices = self.conn.execute(f'select price from order_units where order_id = {self.idx}').fetchall()
        return sum(p[0] for p in prices)

    def update_total(self):
        total = self.get_total()
        self.doubleSpinBox.setValue(total)

    def open_unit_dialog(self, *args, **kwargs):
        self.sub = QtWidgets.QMainWindow()
        self.sub_ui = OrderUnitDialog(self, *args, **kwargs)
        self.sub_ui.setupUi(self.sub)
        self.sub.show()

    def create_unit(self):
        self.open_unit_dialog(self.conn)

    def delete_all_units(self):
        self.conn.execute(f'delete from order_units where order_id = {self.idx}')
        self.conn.commit()

    def get_chosen_unit_id(self):
        row = get_focused_row(self.tableWidget)
        if row is None:
            return None
        order_unit_idx = self.conn.execute(f'select id from order_units where order_id = {self.idx} limit 1 offset {row}').fetchone()[0]
        return order_unit_idx

    def delete_unit(self):
        idx = self.get_chosen_unit_id()
        if idx is None:
            return error('Сначала нужно выбрать позицию!')
        self.conn.execute(f'delete from order_units where id = {idx}')
        self.conn.commit()
        self.update_all()


    def edit_unit(self):
        idx = self.get_chosen_unit_id()
        if idx is None:
            return error('Сначала нужно выбрать позицию!')
        self.open_unit_dialog(self.conn, idx=idx)

    def update_unit_table(self):
        r = f'''select t.id, h.name, ou.total, ou.people from order_units as ou join tours as t on t.id == tour_id join hotels as h on h.id == t.hotel_id where ou.order_id = {self.idx}'''
        res = self.conn.execute(r).fetchall()
        self.tableWidget.setRowCount(len(res))
        for i in range(len(res)):
            res1 = [f'Т. {res[i][0]}, "{res[i][1]}"', res[i][2], res[i][3]]
            for j in range(len(res1)):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(res1[j])))

    def update_all(self):
        self.update_unit_table()
        self.update_total()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация заказа"))
        self.label.setText(_translate("MainWindow", "Клиент"))
        self.label_2.setText(_translate("MainWindow", "Тип оплаты"))
        self.label_3.setText(_translate("MainWindow", "Заказанные туры:"))
        self.pushButton_5.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_4.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_3.setText(_translate("MainWindow", "Удалить"))
        self.label_4.setText(_translate("MainWindow", "Итого (руб)"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))
        self.pushButton.setText(_translate("MainWindow", "ОК"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = OrderDialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
