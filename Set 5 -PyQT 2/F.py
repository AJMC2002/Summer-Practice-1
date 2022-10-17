import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw, QtGui as qtg, QtCore as qtc
from C import FilmsSearch


class WinAddFilm(qtw.QDialog):
    def __init__(self, uiFile, db, parent=None):
        super().__init__(parent, qtc.Qt.WindowSystemMenuHint)
        self.db = db
        uic.loadUi(uiFile, self)

        self.name.setMaxLength(1000)
        self.year.setValidator(qtg.QRegExpValidator(qtc.QRegExp("[1-2][0-9]*")))
        self.year.setMaxLength(4)
        self.genre.setValidator(qtg.QRegExpValidator(qtc.QRegExp("[a-z-A-Z_]+")))
        self.duration.setValidator(qtg.QRegExpValidator(qtc.QRegExp("[1-9][0-9]*")))
        self.duration.setMaxLength(10)

        con = sqlite3.connect(self.db)
        cur = con.cursor()
        for id, title in cur.execute("SELECT * FROM genres").fetchall():
            self.genre.addItem(title.upper(), id)
        con.close()

        self.resetBtn.clicked.connect(lambda: self.reset())
        self.saveBtn.clicked.connect(lambda: self.save())
        self.discardBtn.clicked.connect(lambda: self.discard())

    def reset(self):
        self.name.clear()
        self.year.clear()
        self.genre.setCurrentIndex(0)
        self.duration.clear()

    def save(self):
        if self.name.text() and self.year.text() and self.duration.text():
            con = sqlite3.connect(self.db)
            cur = con.cursor()
            if self.genre.currentData() is not None:
                genre_id = self.genre.currentData()
            else:
                new_genre = self.genre.currentText()
                print(new_genre)
                cur.execute(
                    "INSERT INTO genres (title) VALUES(?);",
                    (new_genre),
                )
                con.commit()
                genre_id = cur.lastrowid

            print("ROWID", genre_id)

            name = self.name.text().strip()
            year = int(self.year.text())
            duration = int(self.duration.text())

            isInDB = cur.execute(
                "SELECT EXISTS(SELECT 1 FROM Films WHERE (title=?) AND (year=?) AND (genre=?) AND (duration=?));",
                (name, year, genre_id, duration),
            ).fetchone()[0]

            if isInDB:
                con.close()
                qtw.QMessageBox.warning(
                    self, "Ошибка!", "Введенный вами фильм уже есть в базе данных."
                )
            else:
                cur.execute(
                    "INSERT INTO Films (title,year,genre,duration) VALUES(?,?,?,?);",
                    (name, year, genre_id, duration),
                )
                con.commit()
                con.close()
                self.accept()
        else:
            qtw.QMessageBox.warning(
                self, "Ошибка!", "Полностью заполните показанные поля."
            )

    def discard(self):
        self.reject()


class FilmsAdd(FilmsSearch):
    def __init__(self, uiFile_main, uiFile_add):
        super().__init__(uiFile_main)

        self.addButton.clicked.connect(lambda: self.openAdd(uiFile_add))

    def updateGenres(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        for id, title in cur.execute("SELECT * FROM genres").fetchall():
            if self.searchItems.findText(title.upper()) == -1:
                self.searchItems.addItem(title.upper(), id)
        con.close()

    def openAdd(self, uiFile_add):
        WinAddFilm(uiFile_add, self.db, self).exec_()
        self.updateGenres()
        self.updateTable()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = FilmsAdd("filmsF.ui", "filmsF-add.ui")
    sys.exit(app.exec_())
