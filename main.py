import sys
import os
import sqlite3
from location import *
from hotel import *
from PyQt5.QtWidgets import (QWidget, QApplication, QTabWidget, 
    QLabel, QVBoxLayout, QTableWidget, QPushButton, QListWidget, QHBoxLayout,
    QTableWidgetItem, QAbstractItemView, QHeaderView)
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QRect
from manager import *
from order_sells import *
from tour import *
from contacts import *
from clients import *
from order import *
from order_payment import *


class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.edit_row = 0
        self.conn = None
        self.load_db()
        self.setupUi()
    
    def load_db(self):
        is_new = not os.path.exists('data.db')
        self.conn = sqlite3.connect('data.db')
        self.conn.execute('''
            create table if not exists locations(
                id integer not null primary key,
                name nvarchar(100) not null
            );''')
        self.conn.execute('''
            create table if not exists managers (
                id integer not null primary key,
                name nvarchar(50) not null,
                phone nvarchar(20),
                email nvarchar(30)
            )''')
        self.conn.execute('''
            create table if not exists hotels(
                id integer not null primary key,
                name nvarchar(200) not null,
                manager_id integer not null default 1,
                contact_phone nvarchar(20),
                location_id integer not null default 1,
                description nvarchar(500),
                foreign key(manager_id) references managers(id) on delete set default,
                foreign key(location_id) references locations(id) on delete set default
            )
        ''')
        self.conn.execute('''
            create table if not exists contacts(
                id integer not null primary key,
                name nvarchar(60) not null,
                phone nvarchar(60) not null
            )
        ''')
        self.conn.execute('''
            create table if not exists clients(
                id integer not null primary key,
                contact_id integer not null default 1,
                name nvarchar(100) not null,
                type nvarchar(50) not null,
                foreign key(contact_id) references contacts(id) on delete set default
            )
        ''')
        self.conn.execute('''
            create table if not exists tours(
                id integer primary key not null,
                hotel_id integer default 1,
                date_in nvarchar(50),
                date_out nvarchar(50),
                day_count integer,
                price float,
                eating_type nvarchar(50),
                foreign key (hotel_id) references hotels(id) on delete set default
            )
        ''')
        self.conn.execute('''
            create table if not exists orders(
                id integer not null primary key,
                client_id integer not null default 1,
                payment_type nvarchar(20),
                total real not null,
                result nvarchar(20) not null default "Действует",
                confirmed_book nvarchar(3) not null default "Нет",
                foreign key (client_id) references clients(id) on delete set default
            )
        ''')
        
        self.conn.execute('''
            create table if not exists order_units(
                id integer not null primary key,
                tour_id integer not null default 1,
                price real not null,
                people integer not null,
                total real not null,
                order_id integer not null default 1,
                foreign key(order_id) references orders(id) on delete set default, 
                foreign key(tour_id) references tours(id) on delete set default
            )
        ''')

        if is_new:
            self.conn.execute(f'''
                insert into managers(name, phone, email)
                values("{IDN}", "{IDN}", "{IDN}")
            ''')
            self.conn.execute(f'''
                insert into locations(name)
                values("{IDN}")
            ''')
            self.conn.execute(f'''
                insert into contacts(name, phone)
                values("{IDN}", "{IDN}")
            ''')
            self.conn.execute(f'''
                insert into hotels(name, manager_id, contact_phone, location_id, description)
                values("{IDN}", 1, "{IDN}", 1, "")
            ''')

        self.conn.commit()

    def table_with_identity(self, tabname):
        if tabname in ['tours', 'orders', 'orders_payment', 'orders_sells']:
            return False
        return True

    def content_request(self, table_name, idx=None):
        if table_name == 'tours':
            r = '''select h.name, date_in, date_out, day_count, eating_type, 
                price, description from tours as t join hotels as h on t.hotel_id = h.id'''
        elif table_name == 'hotels':
            r = '''select h.name, l.name, m.name, h.contact_phone, h.description
                from hotels as h join locations as l on l.id = h.location_id
                join managers as m on m.id = h.manager_id'''
        elif table_name == 'managers':
            r = '''select name, phone, email from managers as m'''
        elif table_name == 'locations':
            r = '''select name from locations as l'''
        elif table_name == 'clients':
            r = '''select c.name, con.name, con.phone, c.type from clients as c join contacts as con on c.contact_id=con.id'''
        elif table_name == 'contacts':
            r = '''select name, phone from contacts as c'''
        elif table_name == 'orders':
            r = '''select c.name, payment_type, total, o.result, o.confirmed_book from orders as o join clients as c on c.id=client_id'''
        elif table_name == 'orders_payment':
            r = '''select row_number() over (order by o.id), o.total, o.result from orders as o'''
        elif table_name == 'orders_sells':
            r = '''select row_number() over (order by o.id), o.total, o.result, o.confirmed_book from orders as o'''

        if idx is None and self.table_with_identity(table_name):
            r += f' where {table_name[0]}.id != 1'
        elif idx is not None:
            r += f' where {table_name[0]}.id = {idx}'
        return r

    def fill_table(self, table_name):
        table = self.get_tab_by_tabname(table_name)
        rows = self.conn.execute(self.content_request(table_name)).fetchall()
        table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(v)))

    def resize_cols(self, table, cols):
        for i, c in enumerate(cols):
            table.setColumnWidth(i, max(10 * len(c), 150))
    
    def setupUi(self):
        self.setWindowTitle('Отели')
        self.setMinimumSize(950, 300)
        self.setMaximumSize(1200, 600)
        self.resize(950, 400)
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 7)
        tabwidget = QTabWidget()
        layout.addWidget(tabwidget)
        
        self.tab1 = QTableWidget()
        self.tab1.setColumnCount(5)
        cols1 = ['Название', 'Местонахождение', 'ФИО менеджера',
            'Контактный телефон', 'Описание']
        self.tab1.setHorizontalHeaderLabels(cols1)
        self.resize_cols(self.tab1, cols1)
        tabwidget.addTab(self.tab1, 'Отели')
        self.tab2 = QTableWidget()
        self.tab2.setColumnCount(3)
        cols2 = ['ФИО', 'Телефон', 'Email']
        self.tab2.setHorizontalHeaderLabels(cols2)
        self.resize_cols(self.tab2, cols2)
        tabwidget.addTab(self.tab2, 'Менеджеры')
        self.tab3 = QTableWidget()
        self.tab3.setColumnCount(1)
        self.resize_cols(self.tab3, ['Название региона'])
        self.tab3.setHorizontalHeaderLabels(['Название региона'])
        tabwidget.addTab(self.tab3, 'Регионы')

        self.tab4 = QTableWidget()
        self.tab4.setColumnCount(7)
        cols4 = ['Отель', 'Дата заезда', 'Дата выезда',
            'Длительность', 'Вид питания', 'Стоимость', 'Описание']
        self.resize_cols(self.tab4, cols4)
        self.tab4.setHorizontalHeaderLabels(cols4)
        tabwidget.addTab(self.tab4, 'Туры')
        
        self.tab5 = QTableWidget()
        self.tab5.setColumnCount(2)
        cols5 = ['Наименование', 'Телефон']
        self.resize_cols(self.tab5, cols5)
        self.tab5.setHorizontalHeaderLabels(cols5)
        tabwidget.addTab(self.tab5, 'Контактные лица')

        self.tab6 = QTableWidget()
        self.tab6.setColumnCount(4)
        cols6 = ['Наименование', 'Контактное лицо',
            'Контактный телефон', 'Вид клиента']
        self.resize_cols(self.tab6, cols6)
        self.tab6.setHorizontalHeaderLabels(cols6)
        tabwidget.addTab(self.tab6, 'Клиенты')

        self.tab7 = QTableWidget()
        self.tab7.setColumnCount(5)
        cols7 = ['Клиент', 'Тип оплаты', 'Стоимость', 'Статус', 'Бронь подтверждена']
        self.tab7.setHorizontalHeaderLabels(cols7)
        self.resize_cols(self.tab7, cols7)
        tabwidget.addTab(self.tab7, 'Заказы')

        self.tab8 = QTableWidget()
        self.tab8.setColumnCount(3)
        cols8 = ['Номер заказа', 'Стоимость', 'Статус']
        self.tab8.setHorizontalHeaderLabels(cols8)
        self.resize_cols(self.tab8, cols8)
        tabwidget.addTab(self.tab8, 'Оплата туров')

        self.tab9 = QTableWidget()
        self.tab9.setColumnCount(4)
        cols9 = ['Номер заказа', 'Стоимость', 'Статус', 'Бронь подтверждена']
        self.tab9.setHorizontalHeaderLabels(cols9)
        self.resize_cols(self.tab9, cols9)
        tabwidget.addTab(self.tab9, 'Продажа туров')

        self.tabwidget = tabwidget
        self.tabwidget.currentChanged.connect(self.tab_changed)

        bottom = QHBoxLayout()
        self.newbutt = QPushButton()
        self.newbutt.clicked.connect(self.create)
        self.newbutt.setText('Создать')
        self.deletebutt = QPushButton()
        self.deletebutt.clicked.connect(self.delete)
        self.deletebutt.setText('Удалить')
        self.editbutt = QPushButton()
        self.editbutt.clicked.connect(self.edit)
        self.editbutt.setText('Редактировать')
        for butt in [self.newbutt, self.editbutt, self.deletebutt]:
            butt.setFixedWidth(105)
            butt.setFixedHeight(23)
            bottom.addWidget(butt)
        layout.addLayout(bottom)
        self.setLayout(layout)
        self.dialogs = [HotelDialog, ManagerDialog, LocationDialog,
            TourDialog, ContactDialog, ClientDialog, OrderDialog, OrderPaymentDialog, OrderSellsDialog]
        self.tabnames = ['hotels', 'managers', 'locations',
            'tours', 'contacts', 'clients', 'orders', 'orders_payment', 'orders_sells']

        for i, name in enumerate(self.tabnames):
            tab = tabwidget.widget(i)
            tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
            tab.doubleClicked.connect(self.dbclick)
            self.fill_table(name)

    def tab_changed(self):
        tab = self.tabnames[self.tabwidget.currentIndex()]
        if tab in ['orders_payment', 'orders_sells']:
            self.newbutt.setEnabled(False)
            self.deletebutt.setEnabled(False)
        else:
            self.newbutt.setEnabled(True)
            self.deletebutt.setEnabled(True)

    def get_tab_by_tabname(self, tabname):
        return self.tabwidget.widget(self.tabnames.index(tabname))

    def create(self):
        curr = self.tabwidget.currentIndex()
        self.openwin(self.dialogs[curr], self.conn)

    def delete(self):
        curr = self.tabwidget.currentIndex()
        table_name = self.tabnames[curr]
        if table_name in ['orders_sells', 'orders_payment']:
            table_name = 'orders'
        table = self.tabwidget.widget(curr)
        fr = get_focused_row(table)
        if fr is None:
            return
        idx = get_id_by_row(self.conn, table_name, fr,
            offset=self.table_with_identity(table_name))
        self.conn.execute(f'delete from {table_name} where id={idx}')

        to_update = None

        if curr == 0: to_update = 'tours'
        elif curr == 1 or curr == 2: to_update = 'hotels'
        elif curr == 4: to_update = 'clients'

        if to_update is not None:
            pid = table_name[:-1] + '_id'
            self.conn.execute(f'update {to_update} set {pid}=1 where {pid}={idx}')
        
        self.conn.commit()
        self.fill_table(table_name)
        if to_update is not None:
            self.fill_table(to_update)

    def get_data_from_row(self, table, row):
        data = []
        for j in range(table.columnCount()):
            data.append(table.item(row, j).text())
        return data

    def edit(self):
        curr = self.tabwidget.currentIndex()
        tab = self.tabwidget.widget(curr)
        fr = get_focused_row(tab)
        if fr is None:
            return
        self.edit_row = fr
        interface = self.dialogs[curr]
        self.openwin(interface, self.conn, row=fr)

    def dbclick(self):
        self.edit()

    def append_table(self, table, items):
        idx = table.rowCount()
        table.insertRow(idx)
        for j, v in enumerate(items):
            table.setItem(idx, j, QTableWidgetItem(str(v)))

    def fill_row_with(self, table, row_idx, data):
        for j, v in enumerate(data):
            table.setItem(row_idx, j, QTableWidgetItem(str(v)))

    def update_at_row(self, dbtab, row):
        table = self.get_tab_by_tabname(dbtab)
        idx = get_id_by_row(self.conn, dbtab, row, offset=self.table_with_identity(dbtab))
        req = self.content_request(dbtab, idx=idx)
        data = self.conn.execute(req).fetchone()
        self.fill_row_with(table, row, data)

    def update_table(self, dbtab):
        self.fill_table(dbtab)

    def add_last(self, dbtab):
        table = self.get_tab_by_tabname(dbtab)
        req = self.content_request(dbtab) + f' order by {dbtab[0]}.id desc limit 1'
        last_row = self.conn.execute(req).fetchone()
        self.append_table(table, last_row)

    def openwin(self, t, *args, **kwargs):
        self.sub = QtWidgets.QMainWindow()
        self.sub_ui = t(self, *args, **kwargs)
        self.sub_ui.setupUi(self.sub)
        self.sub.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())