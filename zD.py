def gematria(word):
    return sum([ord(c) - ord("A") + 1 for c in word.upper()])


words = []

while True:
    try:
        w = input()
        words.append(w)
    except EOFError:
        break

print(*sorted(words, key=lambda x: (gematria(x), x)), sep="\n")
