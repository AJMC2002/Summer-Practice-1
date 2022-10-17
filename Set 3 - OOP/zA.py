class Balance:
    def __init__(self):
        self.r = 0
        self.l = 0

    def add_right(self, x):
        self.r += x

    def add_left(self, x):
        self.l += x

    def result(self):
        if self.r == self.l:
            return "="
        elif self.r > self.l:
            return "R"
        else:
            return "L"


balance = Balance()
balance.add_right(10)
balance.add_left(9)
balance.add_left(2)
print(balance.result())

balance = Balance()
balance.add_right(10)
balance.add_left(5)
balance.add_left(5)
print(balance.result())
balance.add_left(1)
print(balance.result())
