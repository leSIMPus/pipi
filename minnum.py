a = int(input("Введите первое число: "))
b = int(input("Введите второе число: "))
c = int(input("Введите третье число: "))

minnum = a
if b < minnum:
    minnum = b
if c < minnum:
    minnum = c

print(f"Минимальное число: {minnum}.")