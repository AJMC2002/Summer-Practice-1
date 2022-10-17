# Задача №3763. Права доступа
methods = {"write": "W", "read": "R", "execute": "X"}
files = {}

N = int(input())
for _ in range(N):
    data = input().split()
    files[data[0]] = data[1:]

M = int(input())
for _ in range(M):
    method, file = input().split()
    if methods[method] in files[file]:
        print("OK")
    else:
        print("Access denied")
