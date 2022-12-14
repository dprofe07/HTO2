from PyQt5 import QtCore, QtGui, QtWidgets
from toolz import *


class LocationDialog(object):
    def __init__(self, parent, conn, row=None):
        super(LocationDialog, self).__init__()
        self.conn = conn
        self.parent = parent
        self.row = row
        self.idx = get_id_by_row(conn, 'locations', row, True)

    def submit(self):
        name = self.lineEdit.text()
        if not strweight(name):
            return error('Не введено название региона!')
        if not self.edit and self.conn.execute(f'select * from locations where name = "{name}"').fetchone() is not None:
            return error('Менеджен с таким ФИО уже записан!')
        
        if not self.edit:
            self.conn.execute(f'insert into locations(name) values("{name}")')
            self.conn.commit()
            self.parent.add_last('locations')
        else:
            self.conn.execute(f'''update locations set name="{name}" where id={self.idx}''')
            self.conn.commit()
            self.parent.update_at_row('locations', self.row)
            self.parent.fill_table('hotels')
        
        self.win.close()

    def prepare(self):
        if self.row is not None:
            self.edit = True
            d = self.conn.execute(f'select name from locations where id = {self.idx}').fetchone()[0]
            self.lineEdit.setText(d)
        else:
            self.edit = False
    
    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(347, 101)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 70, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(266, 70, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.submit)
        self.pushButton.clicked.connect(MainWindow.close)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 331, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 151, 21))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.prepare()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация расположения"))
        self.pushButton.setText(_translate("MainWindow", "Отмена"))
        self.pushButton_2.setText(_translate("MainWindow", "ОК"))
        self.label.setText(_translate("MainWindow", "Введите имя региона:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
