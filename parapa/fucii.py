import math
def cca(radius):
    return math.pi * radius ** 2
def ip(number):
    return number > 0

r = int(input("Введите радиус круга: "))
print(f"Площадь такого круга: {cca(r)}")
c = int(input("Введите число: "))
print(ip(c))