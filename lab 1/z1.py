
class Student:
    def __init__(self, name,  group, grades):
        self.name = name
        self.group = group
        self.grades = grades

    def avg(self):
        return sum(self.grades) / len(self.grades)

    def ie(self):
        return self.avg() >= 4.5

students = []
with open("students.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            name, group, grades_str = line.split(";")
            grades = list(map(int, grades_str.split(",")))
            students.append(Student(name, group, grades))

with open("excellent_students.txt", "w", encoding="utf-8") as f:
    for student in students:
        if student.ie():
            f.write(f"{student.name} - {student.group}\n")

from  collections import defaultdict
group_grades = defaultdict(list)
for student in students:
    group_grades[student.group].append(student.avg())
for group, averages in group_grades.items():
    group_average = sum(averages) / len(averages)
    print(f"Средний балл группы {group}: {group_average:2f}")