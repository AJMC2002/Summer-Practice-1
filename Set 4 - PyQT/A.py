import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg


class Window(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.title = "HTML Interpreter"
        self.top = 200
        self.left = 500
        self.width = 500
        self.height = 700

        self.__Window()

    def __Window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setLayout(qtw.QVBoxLayout())

        label = qtw.QLabel("HTML Interpreter")
        label.setFont(qtg.QFont("Times New Roman", 20, weight=75))

        plainText = qtw.QPlainTextEdit()
        plainText.setPlaceholderText("Insert HTML text")
        plainText.setFont(qtg.QFont("Roboto", 13))

        btn_translate = qtw.QPushButton("Translate", clicked=lambda: insertHTML())
        btn_clear = qtw.QPushButton("Clear", clicked=lambda: clearText())

        textBrowser = qtw.QTextBrowser()
        textBrowser.setOpenExternalLinks(True)

        self.layout().addWidget(label)
        self.layout().addWidget(plainText)
        self.layout().addWidget(btn_translate)
        self.layout().addWidget(btn_clear)
        self.layout().addWidget(textBrowser)
        self.show()

        def insertHTML():
            textBrowser.clear()
            textBrowser.insertHtml(plainText.toPlainText())

        def clearText():
            plainText.setPlainText("")


App = qtw.QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
