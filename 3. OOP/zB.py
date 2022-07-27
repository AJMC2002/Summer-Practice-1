class MyVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"MyVector({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def __add__(self, v):
        return MyVector(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return MyVector(self.x + v.x, self.y + v.y)

    def __mul__(self, k):
        return MyVector(k * self.x, k * self.y)

    def __rmul__(self, k):
        return self.__mul__(k)

    def __imul__(self, k):
        self.x *= k
        self.y *= k
        return self

    def __abs__(self):
        return (self.x**2 + self.y**2) ** 0.5


v1 = MyVector(-2, 5)
v2 = MyVector(3, -4)
v_sum = v1 + v2
print(v_sum)
