class Polynomial:
    def __init__(self, coefficients):
        self.coeffs = coefficients.copy()

    def __call__(self, x):
        return sum([coeff * x**deg for deg, coeff in enumerate(self.coeffs)])

    def __add__(self, poly):
        new_coeffs = [sum(el) for el in zip(self.coeffs, poly.coeffs)]
        if len(self.coeffs) > len(poly.coeffs):
            new_coeffs += self.coeffs[len(poly.coeffs) :]
        else:
            new_coeffs += poly.coeffs[len(self.coeffs) :]
        return Polynomial(new_coeffs)


a = [1, 2, 3, 4]
pol = Polynomial(a)
a.append(10)
print(pol(10))
