student = {
    "name": "Антон",
    "age": 19,
    "course": "Pipon",
    "grades": [4,5,3,5,4]
}
print(f"Имя студента: {student['name']}\nКурс студента: {student['course']}")

grades = student["grades"]
ave = sum(grades) / len(grades)
print(f"Средни балл студента: {ave}")

student["grades"].append(5)
print(f"Обновленная информация: {student}")
