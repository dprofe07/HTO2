from PyQt5 import QtCore, QtGui, QtWidgets

from toolz import get_id_by_row


class OrderPaymentDialog(object):
    def __init__(self, parent, conn, row=None):
        super().__init__()
        self.parent = parent
        self.conn = conn
        self.row = row
        self.edit = row is not None

    def submit(self):
        id_ = 0
        id_with_rn = self.conn.execute(f'''select row_number() over (order by id), id from orders''').fetchall()

        for i in id_with_rn:
            if i[0] == self.cmbOrder.currentIndex() + 1:
                id_ = i[1]
                break
        self.conn.execute(f'''
            update orders
            set result = "{self.cmbStatus.currentText()}" 
            where id = {id_}
        ''')
        self.conn.commit()
        self.parent.update_table('orders_payment')
        self.parent.update_table('orders')
        self.parent.update_table('orders_sells')
        self.win.close()

    def prepare(self):
        req = '''
            select row_number() over (order by o.id), o.id
            from orders as o 
        '''
        lst_orders = self.conn.execute(req).fetchall()
        hotels = []
        for ord in lst_orders:
            hotels_req = f'''
            select h.name 
            from order_units as ou
            join tours t on t.id = ou.tour_id 
            join hotels h on h.id = t.hotel_id 
            where ou.order_id = {ord[1]} '''
            hotels.append(self.conn.execute(hotels_req).fetchall())
        orders = [f'№{o[0]}, с отелями: ' + ', '.join(h[0] for h in hs) for o, hs in zip(lst_orders, hotels)]

        for i in orders:
            self.cmbOrder.addItem(i)

        self.cmbStatus.addItems(['Действует', 'Оплачен', 'Отменён'])

        if self.edit:
            self.cmbOrder.setCurrentIndex(self.row)
            self.cmbOrder.setEnabled(False)
        id_ = 0
        id_with_rn = self.conn.execute(f'''select row_number() over (order by id), id from orders''').fetchall()

        for i in id_with_rn:
            if i[0] == self.cmbOrder.currentIndex() + 1:
                id_ = i[1]
                break

        status = self.conn.execute(f'''select result from orders where id = {id_}''').fetchone()[0]
        self.cmbStatus.setCurrentText(status)

    def cmb_changed(self):
        id_ = 0
        id_with_rn = self.conn.execute(f'''select row_number() over (order by id), id from orders''').fetchall()

        for i in id_with_rn:
            if i[0] == self.cmbOrder.currentIndex() + 1:
                id_ = i[1]
                break

        status = self.conn.execute(f'''select result from orders where id = {id_}''').fetchone()[0]
        self.cmbStatus.setCurrentText(status)

    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(442, 106)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 21))
        self.label.setObjectName("label")
        self.cmbOrder = QtWidgets.QComboBox(self.centralwidget)
        self.cmbOrder.setGeometry(QtCore.QRect(70, 10, 361, 25))
        self.cmbOrder.setObjectName("comboBox")
        self.cmbOrder.currentIndexChanged.connect(self.cmb_changed)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 51, 17))
        self.label_2.setObjectName("label_2")
        self.cmbStatus = QtWidgets.QComboBox(self.centralwidget)
        self.cmbStatus.setGeometry(QtCore.QRect(70, 40, 361, 25))
        self.cmbStatus.setEditable(False)
        self.cmbStatus.setObjectName("comboBox_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(378, 80, 61, 21))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 80, 89, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.win.close)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.prepare()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Оплата заказа"))
        self.label.setText(_translate("MainWindow", "Заказ"))
        self.label_2.setText(_translate("MainWindow", "Статус"))
        self.pushButton.setText(_translate("MainWindow", "ОК"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))
