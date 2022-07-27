def isPrime(n: str):
    n = int(n)
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def isPalindrome(n: str):
    return n == n[::-1]


def isPow2(n: str):
    n = int(n)
    return n and not (n & n - 1)


def check_pin(pinCode: str):
    a, b, c = pinCode.split("-")
    if isPrime(a) and isPalindrome(b) and isPow2(c):
        return "Корректен"
    else:
        return "Некорректен"


print(check_pin("7-101-4"))
print(check_pin("12-22-16"))
