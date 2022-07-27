# Задача №111385. Сапер
N, M, K = map(int, input().split())
mines = [list(map(int, input().split())) for _ in range(K)]
field = [[0 for _ in range(M + 2)] for _ in range(N + 2)]

for i in range(1, N + 1):
    for j in range(1, M + 1):
        if [i, j] in mines:
            sub_is = [i - 1, i, i + 1]
            sub_js = [j - 1, j, j + 1]
            for sub_i in sub_is:
                for sub_j in sub_js:
                    field[sub_i][sub_j] += 1

for i, j in mines:
    field[i][j] = "*"

for row in field[1 : N + 1]:
    print(*row[1 : M + 1])
