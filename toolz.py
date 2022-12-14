from PyQt5.QtWidgets import QMessageBox

IDN = 'Н/У'
errbox = None

def error(err):
    global errbox
    errbox = QMessageBox()
    errbox.setIcon(QMessageBox.Critical) 
    errbox.setText(err)
    errbox.setWindowTitle('Ошибка!')
    errbox.show()

def strweight(s):
    for ch in s:
        if ch not in [' ', '\n']:
            return True
    return False

def get_id_by_row(conn, table_name, row, offset=False):
    if row is None:
        return None
    elif offset:
        row += 1
    return conn.execute(f'select id from {table_name} limit 1 offset {row}').fetchone()[0]


def get_focused_row(tab):
    si = tab.selectedItems()
    if not si:
        return None
    row = si[0].row()
    for i in si[1:]:
        if i.row() != row:
            return None
    return row