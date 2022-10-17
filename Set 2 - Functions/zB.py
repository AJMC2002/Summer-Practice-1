def simple_map(operation, values):
    return [operation(val) for val in values]


values = [1, 3, 1, 5, 7]
operation = lambda x: x + 5
print(*simple_map(operation, values))
