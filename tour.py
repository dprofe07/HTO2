from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from datetime import date
from toolz import *

class TourDialog(object):
    def __init__(self, parent, conn, row=None):
        super(TourDialog, self).__init__()
        self.parent = parent
        self.conn = conn
        self.row = row
        self.idx = get_id_by_row(conn, 'tours', row)
        self.date_in = QDate.currentDate()
        self.date_out = QDate.currentDate().addDays(1)
        self.days_count = 0
        self.ptr = 0

    def prepare(self):
        if self.idx is not None:
            self.edit = True
            d = self.parent.content_request('tours', self.idx)
            data = self.conn.execute(d).fetchone()
            hotel_name, date_in_s, date_out_s, _, eat_type, price, _ = data
            self.comboBox.setCurrentText(hotel_name)
            self.date_in = self.str_to_date(date_in_s)
            self.date_out = self.str_to_date(date_out_s)
            self.comboBox_2.setCurrentText(eat_type)
            self.doubleSpinBox.setValue(price)
        else:
            self.edit = False
        self.update_description()
        self.update_days_count()
    
    def date_to_str(self, date):
        return '{0}.{1}.{2}'.format(date.day(), date.month(), date.year())

    def str_to_date(self, s):
        p = [int(i) for i in s.split('.')]
        return QDate(*p[::-1])

    def submit(self):
        hotel_id = self.comboBox.currentIndex()
        hotel_id = get_id_by_row(self.conn, 'hotels', hotel_id)
        eat_type = self.comboBox_2.currentText()
        price = self.doubleSpinBox.value()
        date_in_str = self.date_to_str(self.date_in)
        date_out_str = self.date_to_str(self.date_out)

        if self.days_count == 0:
            return error('Выбран неверный период пребывания!')
        
        if self.edit:
            self.conn.execute(f'''update tours set hotel_id={hotel_id}, price={price}, 
                eating_type="{eat_type}", date_in="{date_in_str}", date_out="{date_out_str}", day_count={self.days_count} where id={self.idx}''')
            self.conn.commit()
            self.parent.update_at_row('tours', self.row)
        else:
            self.conn.execute(f'''insert into tours(hotel_id, price, eating_type, date_in, date_out, day_count)
                values({hotel_id}, {price}, "{eat_type}", "{date_in_str}", "{date_out_str}", {self.days_count})''')
            self.conn.commit()
            self.parent.add_last('tours')
        self.win.close()

    def update_days_count(self):
        delta = self.from_qt_format(self.date_out) - self.from_qt_format(self.date_in)
        self.days_count = max(0, delta.days + 1)
        self.spinBox.setValue(self.days_count)

    def from_qt_format(self, d):
        return date(d.year(), d.month(), d.day())

    def update_calendar(self):
        d = self.calendarWidget.selectedDate()
        if self.ptr == 0:
            self.date_in = d
        else:
            self.date_out = d
        self.update_days_count()
    
    def set_date(self, date):
        self.calendarWidget.setSelectedDate(date)
        self.calendarWidget.setFocus()

    def enable_date(self, i):
        self.ptr = i
        if i == 0:
            self.set_date(self.date_in)
        else:
            self.set_date(self.date_out)

    def update_description(self):
        hotel = self.comboBox.currentText()
        decsr = self.conn.execute(f'select description from hotels where name = "{hotel}"').fetchone()[0]
        self.plainTextEdit.setPlainText(decsr)

    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(450, 425)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 431, 171))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        options = self.conn.execute('select name from hotels').fetchall()
        options = [o[0] for o in options]
        self.comboBox.addItems(options)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(['Без питания', 'Завтрак', '3-х разовое'])
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setMinimum(0)
        self.doubleSpinBox.setMaximum(1e+8)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.plainTextEdit)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(128, 190, 313, 145))
        self.calendarWidget.setObjectName("calendarWidget")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 190, 61, 20))
        self.label_5.setObjectName("label_5")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(10, 217, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 236, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton.clicked.connect(lambda: self.enable_date(0))
        self.radioButton_2.clicked.connect(lambda: self.enable_date(1))
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 350, 101, 22))
        self.label_6.setObjectName("label_6")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(130, 350, 311, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setReadOnly(True)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(367, 390, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 390, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(MainWindow.close)
        self.calendarWidget.clicked.connect(self.update_calendar)
        self.plainTextEdit.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.comboBox.activated.connect(self.update_description)
        self.prepare()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация тура"))
        self.label.setText(_translate("MainWindow", "Отель пребывания"))
        self.label_3.setText(_translate("MainWindow", "Тип питания"))
        self.label_4.setText(_translate("MainWindow", "Стоимость тура (руб)"))
        self.label_2.setText(_translate("MainWindow", "Краткое описание"))
        self.label_5.setText(_translate("MainWindow", "Даты:"))
        self.radioButton.setText(_translate("MainWindow", "Заезда"))
        self.radioButton_2.setText(_translate("MainWindow", "Выезда"))
        self.label_6.setText(_translate("MainWindow", "Время пребывания"))
        self.pushButton.setText(_translate("MainWindow", "ОК"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))