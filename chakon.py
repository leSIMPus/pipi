start = int(input("Введите начальное число: "))
end = int(input("Введите конечное число: "))
diap = []

ch = False
for num in range(start, end+1):
    if num % 2 == 0:
        diap.append(num)
        ch = True
if not ch:
    print("В этом диапазоне нет четных чисел.")
else:
    print(f"Четные числа в диапазоне от {start} до {end}: {diap}")