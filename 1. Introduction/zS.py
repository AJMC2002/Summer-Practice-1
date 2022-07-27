latdic = {}

N = int(input())
for _ in range(N):
    eng, lat_words = input().split(" - ")
    for lat in lat_words.split(", "):
        latdic[lat] = latdic.get(lat, [])
        latdic[lat].append(eng)

print(len(latdic))
for lat, eng_words in sorted(latdic.items()):
    print(lat, "-", ", ".join(sorted(eng_words)))
