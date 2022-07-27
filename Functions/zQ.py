# Задача №3765. Страны и города
cities = {}

N = int(input())
for _ in range(N):
    data = input().split()
    for city in data[1:]:
        cities[city] = data[0]

M = int(input())
for _ in range(M):
    print(cities[input()])
