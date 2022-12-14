from PyQt5 import QtCore, QtGui, QtWidgets
from toolz import *

class ManagerDialog(object):
    def __init__(self, parent, conn, row=None):
        super(ManagerDialog, self).__init__()
        self.parent = parent
        self.conn = conn
        self.row = row
        self.idx = get_id_by_row(conn, 'managers', row, True)

    def submit(self):
        name = self.lineEdit.text()
        phone = self.lineEdit_2.text()
        email = self.lineEdit_3.text()

        if not strweight(name):
            return error('Не введено ФИО!')
        elif not self.edit and self.conn.execute(f'select * from managers where name = "{name}"').fetchone() is not None:
            return error('Такой менеджер уже записан!')
        
        if self.edit:
            self.conn.execute(f'''update managers set name="{name}", phone="{phone}", email="{email}" where id={self.idx}''')
            self.conn.commit()
            self.parent.update_at_row('managers', self.row)
            self.parent.fill_table('hotels')
        else:
            self.conn.execute(f'''insert into managers(name, phone, email) values("{name}", "{phone}", "{email}")''')
            self.conn.commit()
            self.parent.add_last('managers')
        self.win.close()

    def prepare(self):
        if self.row is not None:
            self.edit = True
            data = self.conn.execute(f'select name, phone, email from managers where id = {self.idx}').fetchone()
            for i, inp in enumerate([self.lineEdit, self.lineEdit_2, self.lineEdit_3]):
                inp.setText(data[i])
        else:
            self.edit = False

    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(351, 138)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 331, 92))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(266, 110, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 110, 75, 23))
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(MainWindow.close)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.prepare()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация менеджера отеля"))
        self.label.setText(_translate("MainWindow", "ФИО менеджера"))
        self.label_2.setText(_translate("MainWindow", "Телефон"))
        self.label_3.setText(_translate("MainWindow", "Email"))
        self.pushButton.setText(_translate("MainWindow", "OK"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))

