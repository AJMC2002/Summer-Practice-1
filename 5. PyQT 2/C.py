import sys
import sqlite3
from B import Films
from PyQt5 import QtWidgets as qtw, QtGui as qtg, QtCore as qtc


class FilmsSearch(Films):
    def __init__(self, uiFile):
        super().__init__(uiFile)

        con = sqlite3.connect(self.db)
        cur = con.cursor()
        for id, title in cur.execute("SELECT * FROM genres").fetchall():
            self.searchItems.addItem(title.upper(), id)
        con.close()

        self.searchItems.currentTextChanged.connect(lambda: self.searchGenre())

    def searchGenre(self):
        if self.searchItems.currentText() == "-":
            self.curr_genre = "-"
        else:
            self.curr_genre = self.searchItems.currentData()

        self.pageNum.setText("1")
        self.updatePageLim()
        self.updateTable()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = FilmsSearch("filmssearch.ui")
    sys.exit(app.exec_())
