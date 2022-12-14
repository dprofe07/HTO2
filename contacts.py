from PyQt5 import QtCore, QtGui, QtWidgets
from toolz import *

class ContactDialog(object):
    def __init__(self, parent, conn, row=None):
        super(ContactDialog, self).__init__()
        self.parent = parent
        self.conn = conn
        self.row = row
        self.idx = get_id_by_row(conn, 'contacts', row, True)

    def submit(self):
        name = self.lineEdit.text()
        phone = self.lineEdit_2.text()

        if not strweight(name):
            return error('Не введен наименование!')
        elif not strweight(phone):
            return error('Не введён телефон!')
        elif not self.edit and self.conn.execute(f'select * from contacts where name = "{name}"').fetchone() is not None:
            return error('Такой контакт уже записан!')
        
        if self.edit:
            self.conn.execute(f'''update contacts set name="{name}", phone="{phone}" where id={self.idx}''')
            self.conn.commit()
            self.parent.update_at_row('contacts', self.row)
            self.parent.fill_table('clients')
        else:
            self.conn.execute(f'''insert into contacts(name, phone) values("{name}", "{phone}")''')
            self.conn.commit()
            self.parent.add_last('contacts')
        self.win.close()

    def prepare(self):
        if self.row is not None:
            self.edit = True
            data = self.conn.execute(f'select name, phone from contacts where id = {self.idx}').fetchone()
            for i, inp in enumerate([self.lineEdit, self.lineEdit_2]):
                inp.setText(data[i])
        else:
            self.edit = False

    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(377, 106)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 51))
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
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 75, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(295, 75, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(MainWindow.close)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.prepare()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация контактного лица"))
        self.label.setText(_translate("MainWindow", "Наименование"))
        self.label_2.setText(_translate("MainWindow", "Контактный телефон"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))
        self.pushButton.setText(_translate("MainWindow", "ОК"))
