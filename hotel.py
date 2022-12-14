from PyQt5 import QtCore, QtGui, QtWidgets
from toolz import *


class HotelDialog(object):
    def __init__(self, parent, conn, row=None):
        super(HotelDialog, self).__init__()
        self.conn = conn
        self.parent = parent
        self.load_choices()
        self.row = row
        self.idx = get_id_by_row(conn, 'hotels', row, True)

    def load_choices(self):
        self.available_locations = self.conn.execute('select name from locations').fetchall()
        self.available_managers = self.conn.execute('select name from managers').fetchall()
        for arr in [self.available_locations, self.available_managers]:
            for i in range(len(arr)):
                arr[i] = arr[i][0]
    
    def submit(self):
        hotel_name = self.lineEdit.text()
        location_idx = self.comboBox.currentIndex()
        location_idx = get_id_by_row(self.conn, 'locations', location_idx)
        manager_idx = self.comboBox_2.currentIndex()
        manager_idx = get_id_by_row(self.conn, 'managers', manager_idx)
        contact_phone = self.lineEdit_2.text()
        description = self.plainTextEdit.toPlainText()

        if not strweight(hotel_name):
            return error('Необходимо указать название отеля!')
        elif not strweight(contact_phone):
            return error('Необходимо указать контактный телефон!')
        elif not self.edit and self.conn.execute(f'select * from hotels where name = "{hotel_name}"').fetchone() is not None:
            return error('Отель с таким названием уже записан!')
        
        if not self.edit:
            self.conn.execute(f'''insert into hotels(name, location_id, manager_id, contact_phone, description)
                values ("{hotel_name}", "{location_idx}", "{manager_idx}", "{contact_phone}", "{description}")''')
            self.conn.commit()
            self.parent.add_last('hotels')
        else:
            self.conn.execute(f'''update hotels set name="{hotel_name}", location_id="{location_idx}", manager_id="{manager_idx}",
                contact_phone="{contact_phone}", description="{description}" where id={self.idx}''')
            self.conn.commit()
            self.parent.update_at_row('hotels', self.row)
            self.parent.fill_table('tours')
        self.win.close()
    
    def prepare(self):
        if self.row is not None:
            self.edit = True
            data = self.conn.execute(self.parent.content_request('hotels', self.idx)).fetchone()
            self.lineEdit.setText(data[0])
            self.comboBox.setCurrentText(data[1])
            self.comboBox_2.setCurrentText(data[2])
            self.lineEdit_2.setText(data[3])
            self.plainTextEdit.setPlainText(data[4])
        else: self.edit = False

    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(406, 251)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 391, 201))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.comboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.plainTextEdit)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(325, 220, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 220, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(MainWindow.close)
        MainWindow.setCentralWidget(self.centralwidget)
        self.comboBox.addItems(self.available_locations)
        self.comboBox_2.addItems(self.available_managers)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.prepare()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация отеля"))
        self.label.setText(_translate("MainWindow", "Имя отеля"))
        self.label_2.setText(_translate("MainWindow", "Местонахождение"))
        self.label_4.setText(_translate("MainWindow", "ФИО менеджера"))
        self.label_3.setText(_translate("MainWindow", "Контактный телефон"))
        self.label_5.setText(_translate("MainWindow", "Описание отеля"))
        self.pushButton.setText(_translate("MainWindow", "ОК"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))

