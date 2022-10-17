# Задача №111386. k-мерный список
def exp_list(n):
    if n == 0:
        return 0
    return [exp_list(n - 1), exp_list(n - 1)]


print(exp_list(int(input())))
