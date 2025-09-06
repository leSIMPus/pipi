import random
num = [random.randint(-10, 10) for _ in range(15)]
print(f"Исходный список: {num}")

a = [x for x in num if x > 0]
print(f"Положительный список: {a}")

b = [x**2 for x in num]
print(f"Список квадратов: {b}")
