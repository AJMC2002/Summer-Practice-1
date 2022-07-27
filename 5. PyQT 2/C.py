import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw, QtGui as qtg, QtCore as qtc


class AlignDelegate(qtw.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = qtc.Qt.AlignCenter


class Window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.rowLimit = 10
        self.pageLimit = 0

        uic.loadUi("filmssearch.ui", self)

        self.pageNum.setValidator(qtg.QRegExpValidator(qtc.QRegExp("[1-9][0-9]*")))
        self.pageNum.textChanged.connect(lambda: self.resizeToContents())
        self.pageNum.editingFinished.connect(lambda: self.updateTable())

        self.prev.clicked.connect(lambda: self.changePage(-1))
        self.next.clicked.connect(lambda: self.changePage(1))

        self.show()
        self.updateTable()
        
    def getRequest(self, condition):
        if condition == "-":
            request = "SELECT * FROM Films"
        else:
            request = f"SELECT * from Films WHERE {self.searchItems.text()}"

        con = sqlite3.connect("films.db")
        cur = con.cursor()
        self.entries = len(cur.execute(request).fetchall())
        self.pageLimit = self.entries // 10 + 1
        con.close()

    def resizeToContents(self):
        font = qtg.QFont("MS Shell Dlg 2", 8)
        font.setBold(True)
        empty_space = 23 - qtg.QFontMetrics(font).width("1")
        text_space = qtg.QFontMetrics(font).width(self.pageNum.text())
        self.pageNum.setFixedWidth(empty_space + text_space)

    def adjustTable(self):
        headerx = self.table.horizontalHeader()
        headery = self.table.verticalHeader()

        for i in range(1, self.table.columnCount()):
            if i == 0:
                headerx.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
            headerx.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)
        headerx.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
        for i in range(self.table.rowCount()):
            if i == 0:
                headery.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
            headery.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)

        self.adjustSize()

    def updateTable(self):
        num = int(self.pageNum.text())

        if num > self.pageLimit:
            num = self.pageLimit
            self.pageNum.setText(f"{num}")

        for i in range(self.table.rowCount(), -1, -1):
            self.table.removeRow(i)

        con = sqlite3.connect("films.db")
        cur = con.cursor()
        films = cur.execute(
            f"SELECT title,year,genre,duration FROM Films LIMIT {10*(num-1)}, {self.rowLimit}"
        ).fetchall()
        films.sort()

        for title, year, genre, duration in films:
            title = str(title)
            year = str(year)
            genre = (
                cur.execute(f"SELECT title FROM genres WHERE id={genre}")
                .fetchone()[0]
                .upper()
            )
            duration = str(duration)

            if not title:
                title = "-"
            if not year:
                year = "-"
            if not genre:
                genre = "-"
            if not duration:
                duration = "-"

            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            self.table.setItem(row_pos, 0, qtw.QTableWidgetItem(title))
            self.table.setItem(row_pos, 1, qtw.QTableWidgetItem(year))
            self.table.setItem(row_pos, 2, qtw.QTableWidgetItem(genre))
            self.table.setItem(row_pos, 3, qtw.QTableWidgetItem(duration))

        delegate = AlignDelegate(self.table)
        for i in range(1, self.table.columnCount()):
            self.table.setItemDelegateForColumn(i, delegate)

        con.close()
        self.adjustTable()

    def changePage(self, x):
        if not (self.pageNum.text() == "1" and x == -1):
            self.pageNum.setText(f"{int(self.pageNum.text()) + x}")
            self.updateTable()


app = qtw.QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
