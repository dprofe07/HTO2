from PyQt5 import QtCore, QtGui, QtWidgets
from toolz import *


class OrderUnitDialog(object):
    def __init__(self, parent, conn, idx=None):
        self.conn = conn
        self.parent = parent
        self.idx = idx


    def update_total_price(self):
        price = self.doubleSpinBox.value()
        people = self.spinBox.value()
        self.doubleSpinBox_2.setValue(price * people)

    def submit(self):
        tour_id = self.get_picked_tour_id()
        price = self.doubleSpinBox.value()
        people = self.spinBox.value()
        total = self.doubleSpinBox_2.value()
        
        if not self.edit:
            self.conn.execute(f'''insert into order_units(order_id, tour_id, total, people, price)
                values({self.parent.idx}, {tour_id}, {total}, {people}, {price}) ''')
            self.conn.commit()
        else:
            self.conn.execute(f'''update order_units set tour_id={tour_id}, price={price}, people={people}, total={total} where id={self.idx}''')
            self.conn.commit()
        
        self.parent.update_all()
        self.win.close()

    def get_picked_tour_id(self):
        tour_row = self.comboBox.currentIndex()
        return get_id_by_row(self.conn, 'tours', tour_row, False)

    def prepare(self):
        if self.idx is not None:
            self.edit = True
            tour_id, price, people, total = self.conn.execute(f'''
                select tour_id, price, people, total from order_units
                where id={self.idx}
            ''').fetchone()
            row = self.conn.execute('select id from tours').fetchall().index((tour_id,))
            self.comboBox.setCurrentIndex(row)
            self.doubleSpinBox.setValue(price)
            self.spinBox.setValue(people)
            self.doubleSpinBox_2.setValue(total)
        else:
            self.update_price()
            self.update_total_price()
            self.edit = False

    def update_price(self):
        tour_id = self.get_picked_tour_id()
        price = self.conn.execute(f'select price from tours where id = {tour_id}').fetchone()[0]
        self.doubleSpinBox.setValue(price)

    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(459, 188)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 441, 131))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
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
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox_2.setReadOnly(True)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 150, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 150, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(MainWindow.close)
        self.spinBox.setMinimum(1)
        self.spinBox.setValue(1)
        self.spinBox.setMaximum(1000)

        for sb in self.doubleSpinBox, self.doubleSpinBox_2:
            sb.setMinimum(0)
            sb.setMaximum(1e10)
        
        for sb in self.spinBox, self.doubleSpinBox:
            sb.valueChanged.connect(self.update_total_price)

        all_tours = self.conn.execute('''
            select h.name from tours as t join hotels as h on h.id = t.hotel_id
        ''').fetchall()

        for i, t in enumerate(all_tours):
            self.comboBox.addItem(f'Тур №{i + 1}, отель "{t[0]}"')

        self.prepare()
        self.comboBox.currentIndexChanged.connect(self.update_price)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Оформить тур"))
        self.label.setText(_translate("MainWindow", "Целевой тур"))
        self.label_2.setText(_translate("MainWindow", "Стоимость (за 1 чел) "))
        self.label_3.setText(_translate("MainWindow", "Кол-во человек"))
        self.label_4.setText(_translate("MainWindow", "Итоговая стоимость"))
        self.pushButton.setText(_translate("MainWindow", "ОК"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))
