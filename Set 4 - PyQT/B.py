import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ops = {"+": "+", "-": "-", "*": "×", "/": "÷"}
        self.isEval = False
        self.secretScreen = []

        uic.loadUi("calc.ui", self)

        # Functionality
        self.pBtn_0.clicked.connect(lambda: self.clickNum("0"))
        self.pBtn_1.clicked.connect(lambda: self.clickNum("1"))
        self.pBtn_2.clicked.connect(lambda: self.clickNum("2"))
        self.pBtn_3.clicked.connect(lambda: self.clickNum("3"))
        self.pBtn_4.clicked.connect(lambda: self.clickNum("4"))
        self.pBtn_5.clicked.connect(lambda: self.clickNum("5"))
        self.pBtn_6.clicked.connect(lambda: self.clickNum("6"))
        self.pBtn_7.clicked.connect(lambda: self.clickNum("7"))
        self.pBtn_8.clicked.connect(lambda: self.clickNum("8"))
        self.pBtn_9.clicked.connect(lambda: self.clickNum("9"))
        self.pBtn_opadd.clicked.connect(lambda: self.clickOp("+"))
        self.pBtn_opred.clicked.connect(lambda: self.clickOp("-"))
        self.pBtn_opmul.clicked.connect(lambda: self.clickOp("*"))
        self.pBtn_opdiv.clicked.connect(lambda: self.clickOp("/"))
        self.pBtn_dot.clicked.connect(lambda: self.clickDot())
        self.pBtn_lpar.clicked.connect(lambda: self.clickPar("("))
        self.pBtn_rpar.clicked.connect(lambda: self.clickPar(")"))
        self.pBtn_del.clicked.connect(lambda: self.clickDel())
        self.pBtn_cls.clicked.connect(lambda: self.clickCls())
        self.pBtn_eq.clicked.connect(lambda: self.clickEq())

    def isNum(self, var):
        try:
            float(var)
            return True
        except ValueError:
            return False

    def replaceSymbols(self, exp):
        for pySymb, guiSymb in self.ops.items():
            exp = exp.replace(pySymb, guiSymb)
        return exp

    def write(self):
        if len(self.secretScreen) == 0:
            self.screen.setText("0")
        elif self.isEval:
            self.screen.setText(self.secretScreen[-1])
        else:
            exp = "".join(self.secretScreen)
            if len(exp) < 15:
                self.screen.setText(self.replaceSymbols(exp))
            else:
                self.clickDel()

    def clickNum(self, num):
        if self.isEval:
            self.isEval = False
            self.secretScreen.clear()
            self.secretScreen.append(num)
        else:
            if len(self.secretScreen) == 0:
                self.secretScreen.append(num)
            elif self.isNum(self.secretScreen[-1]):
                self.secretScreen[-1] += num
            elif self.secretScreen[-1] != ")" and self.secretScreen[-1] != "ERROR":
                self.secretScreen.append(num)
        self.write()

    def clickOp(self, op):
        self.isEval = False
        if len(self.secretScreen) > 0:
            if self.isNum(self.secretScreen[-1]) or self.secretScreen[-1] == ")":
                self.secretScreen.append(op)
        else:
            self.secretScreen.append("0")
            self.secretScreen.append(op)
        self.write()

    def clickDot(self):
        if not self.isEval:
            if len(self.secretScreen[-1]) == 0:
                self.secretScreen.append("0.")
            elif self.isNum(self.secretScreen[-1]):
                if "." not in self.secretScreen[-1]:
                    self.secretScreen[-1] += "."
            elif self.secretScreen[-1] != ")" and self.secretScreen[-1] != "ERROR":
                self.secretScreen.append("0.")
        self.write()

    def clickPar(self, par):
        if par == "(":
            if (
                not self.isNum(self.secretScreen[-1])
                and self.secretScreen[-1] != "ERROR"
            ):
                self.secretScreen.append("(")
        elif par == ")":
            if self.isNum(self.secretScreen[-1]) and (
                self.secretScreen.count("(") > self.secretScreen.count(")")
            ):
                self.secretScreen.append(")")
        self.write()

    def clickDel(self):
        if not self.isEval and len(self.secretScreen) > 0:
            if self.isNum(self.secretScreen[-1]):
                self.secretScreen[-1] = self.secretScreen[-1][:-1]
            else:
                self.secretScreen.pop()
        self.write()

    def clickCls(self):
        self.secretScreen.clear()
        self.write()

    def clickEq(self):
        self.isEval = True
        exp = "".join(self.secretScreen)
        if len(self.secretScreen) == 0:
            exp = "0"
        self.secretScreen.clear()
        try:
            if len(f"{eval(exp)}") < 15:
                self.secretScreen.append(f"{eval(exp)}")
            else:
                self.secretScreen.append(f"{eval(exp):5e}")
        except:
            self.secretScreen.append("ERROR")
        self.write()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
