# Задача №112212. Чётные цифры
num = input()
print(sum([int(d) % 2 == 0 for d in num]))
