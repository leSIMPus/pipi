spisok = [12, -5, 23, 0, 4, 17, -8, 0, 11]

print(f"Количество элементов в списке: {len(spisok)}")
print(f"Последний элемент: {spisok[-1]}")
print(f"Список в обратном порядке: {spisok[::-1]}")

if 5 in spisok and 17 in spisok:
    print("Да")
else:
    print("Нет")