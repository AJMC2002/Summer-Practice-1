# Задача №3835. Наименьший положительный
nums = list(map(int, input().split()))
print(min([num for num in nums if num > 0]))
