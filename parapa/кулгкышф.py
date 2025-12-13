while True:
    ui = input("Введите число или 'стоп': ")
    if ui == "стоп":
        break
    try:
        num = float(ui)
        print(f"Вы ввели: {num}")
    except ValueError:
        print("Ошибка: введите число или 'стоп'.")
