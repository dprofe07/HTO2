from PyQt5 import QtCore, QtGui, QtWidgets
from toolz import *


class ClientDialog(object):
    def __init__(self, parent, conn, row=None):
        super(ClientDialog, self).__init__()
        self.conn = conn
        self.parent = parent
        self.row = row
        self.idx = get_id_by_row(conn, 'clients', row)

    def submit(self):
        name = self.lineEdit.text()
        contact_id = self.comboBox.currentIndex()
        contact_id = get_id_by_row(self.conn, 'contacts', contact_id, False)
        type_ = self.comboBox_2.currentText()

        if not strweight(name):
            return error('Не введено наименование!')
        if not self.edit and self.conn.execute(f'select * from clients where name = "{name}"').fetchone() is not None:
            return error('Клиент с таким наименованием уже записан!')
        
        if not self.edit:
            self.conn.execute(f'insert into clients(name, contact_id, type) values("{name}", {contact_id}, "{type_}")')
            self.conn.commit()
            self.parent.add_last('clients')
        else:
            self.conn.execute(f'''update clients set name="{name}", contact_id={contact_id}, type="{type_}" where id={self.idx}''')
            self.conn.commit()
            self.parent.update_at_row('clients', self.row,)
        
        self.win.close()

    def prepare(self):
        if self.row is not None:
            self.edit = True
            r = self.parent.content_request('clients', idx=self.idx)
            data = self.conn.execute(r).fetchone()
            self.lineEdit.setText(data[0])
            self.comboBox.setCurrentText(data[1])
            self.comboBox_2.setCurrentText(data[3])
        else:
            self.edit = False
    
    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(350, 132)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 331, 81))
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
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(185, 100, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(267, 100, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(MainWindow.close)

        contacts = self.conn.execute('select name from contacts').fetchall()
        for c in contacts:
            self.comboBox.addItem(c[0])

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.prepare()
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация клиента"))
        self.label.setText(_translate("MainWindow", "Наименование"))
        self.label_2.setText(_translate("MainWindow", "Контактное лицо"))
        self.label_3.setText(_translate("MainWindow", "Вид клиента"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Физическое лицо"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Юридическое лицо"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))
        self.pushButton.setText(_translate("MainWindow", "ОК"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
