# Задача №3764. Частотный анализ
import sys

text = sys.stdin.readlines()

counter = {}

for line in text:
    line = line.strip("\n").split()
    for word in line:
        counter[word] = counter.get(word, 0) + 1

counter_list = list(zip(counter.values(), counter.keys()))
counter_list.sort(key=lambda tup: (-tup[0], tup[1]))

print(*[word for count, word in counter_list], sep="\n")
