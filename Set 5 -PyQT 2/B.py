import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw, QtGui as qtg, QtCore as qtc


class AlignDelegate(qtw.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = qtc.Qt.AlignCenter


class Films(qtw.QWidget):
    def __init__(self, uiFile):
        super().__init__()
        self.db = "films.db"
        self.rowLim = 10
        self.pageLim = 1
        self.curr_genre = "-"

        uic.loadUi(uiFile, self)

        self.pageNum.setValidator(qtg.QRegExpValidator(qtc.QRegExp("[1-9][0-9]*")))
        self.pageNum.setMaxLength(40)
        self.pageNum.textChanged.connect(lambda: self.resizeToContents())
        self.pageNum.editingFinished.connect(lambda: self.updateTable())

        self.prev.clicked.connect(lambda: self.changePage(-1))
        self.next.clicked.connect(lambda: self.changePage(1))

        qtw.QShortcut(
            qtg.QKeySequence(qtc.Qt.Key_Left),
            self,
            activated=lambda: self.prev.click(),
        )
        qtw.QShortcut(
            qtg.QKeySequence(qtc.Qt.Key_Right),
            self,
            activated=lambda: self.next.click(),
        )

        self.updatePageLim()

        self.show()
        self.updateTable()

    def getRequest(self, limited=True):
        request = "SELECT * FROM Films"
        if self.curr_genre != "-":
            request += f"\nWHERE genre={self.curr_genre}"
        if limited:
            page = int(self.pageNum.text())
            if page > self.pageLim:
                page = self.pageLim
                self.pageNum.setText(f"{page}")
            request += f"\nLIMIT {10*(page-1)}, {self.rowLim}"

            con = sqlite3.connect(self.db)
            cur = con.cursor()
            items = cur.execute(request).fetchall()
            films = []

            for id, title, year, genre, duration in items:
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

                films.append((title, year, genre, duration))
            con.close()
            return films
        else:
            con = sqlite3.connect(self.db)
            cur = con.cursor()
            items = cur.execute(request).fetchall()
            con.close()
            return items

    def updatePageLim(self):
        self.pageLim = len(self.getRequest(limited=False)) // 10 + 1

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

        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.adjustSize()
        self.setFixedHeight(self.height())

    def updateTable(self):
        for i in range(self.table.rowCount(), -1, -1):
            self.table.removeRow(i)

        for title, year, genre, duration in self.getRequest():
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            self.table.setItem(row_pos, 0, qtw.QTableWidgetItem(title))
            self.table.setItem(row_pos, 1, qtw.QTableWidgetItem(year))
            self.table.setItem(row_pos, 2, qtw.QTableWidgetItem(genre))
            self.table.setItem(row_pos, 3, qtw.QTableWidgetItem(duration))

        delegate = AlignDelegate(self.table)
        for i in range(1, self.table.columnCount()):
            self.table.setItemDelegateForColumn(i, delegate)

        self.adjustTable()

    def changePage(self, x):
        if not (self.pageNum.text() == "1" and x == -1):
            self.pageNum.setText(f"{int(self.pageNum.text()) + x}")
            self.updateTable()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = Films("filmsB.ui")
    sys.exit(app.exec_())
