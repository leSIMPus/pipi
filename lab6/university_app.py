import sqlite3

STUDENT_FIELDS = {
    "id": "ID",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "group_name": "Группа",
    "admission_year": "Год поступления",
    "average_grade": "Средний балл",
    "created_at": "Когда добавлен"
}

COURSE_FIELDS = {
    "id": "ID курса",
    "course_name": "Название курса",
    "instructor": "Преподаватель",
    "credits": "Кредиты",
    "created_at": "Когда добавлен"
}


def print_table(rows, field_map):
    if not rows:
        print("Нет данных для отображения.")
        return

    for row in rows:
        print("—" * 35)
        for key, title in field_map.items():
            value = row.get(key, "—")
            print(f"{title}: {value}")
    print("—" * 35)

def create_database():
    try:
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")
        c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        group_name TEXT NOT NULL,
        admission_year INTEGER NOT NULL,
        average_grade REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT UNIQUE NOT NULL,
        instructor TEXT NOT NULL,
        credits INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS student_courses (
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE
        );
        ''')

        print("круто и креветка забивает данк в кольцо")

    except sqlite3.Error as error:
        print("отстой: ", error)

def add_student(first_name, last_name, group_name, admission_year, average_grade=None):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute(
                '''INSERT INTO students (first_name, last_name, group_name, admission_year, average_grade)
                VALUES (?, ?, ?, ?, ?)
                ''', (first_name, last_name, group_name, admission_year, average_grade))
            return c.lastrowid
    except sqlite3.Error as error:
        print("Ошибка при добавлении студента: ", error)
        return None

def get_all_students():
    try:
        with sqlite3.connect('university.db') as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''SELECT * FROM students''')
            return [dict(row) for row in c.fetchall()]
    except sqlite3.Error as error:
        print("Ошибка при получении всех студентов: ", error)
        return []

def get_student_by_group(group_name):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''SELECT * FROM students WHERE group_name = ?''', (group_name,))
            return [dict(row) for row in c.fetchall()]
    except sqlite3.Error as error:
        print("Ошибка при поиске студентов: ", error)
        return []

def update_student_grade(student_id, new_grade):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''
            UPDATE students SET average_grade = ?
            WHERE id = ?
            ''', (new_grade, student_id))
            return c.rowcount > 0
    except sqlite3.Error as error:
        print("Ошибка при добавлении оценки: ", error)
        return False

def delete_student(student_id):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''
            DELETE FROM students WHERE id = ?
            ''', (student_id,))
            return c.rowcount > 0
    except sqlite3.Error as error:
        print("Ошибка при удалении студента: ", error)
        return False

def add_course(course_name, instructor, credits):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''INSERT INTO courses (course_name, instructor, credits)
            VALUES (?, ?, ?)
            ''', (course_name, instructor, credits))
            return c.lastrowid
    except sqlite3.Error as error:
        print("Ошибка при добавлении курса: ", error)
        return None

def enroll_student_in_course(student_id, course_id):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''
            INSERT INTO student_courses (student_id, course_id)
            VALUES (?, ?)
            ''', (student_id, course_id))
            return True
    except sqlite3.Error as error:
        print("Ошибка при записи студента на курс: ", error)
        return False

def get_student_courses(student_id):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''
            SELECT courses.* FROM courses
            JOIN student_courses ON courses.id = student_courses.course_id
            WHERE student_courses.student_id = ?
            ''', (student_id,))
            return [dict(row) for row in c.fetchall()]
    except sqlite3.Error as error:
        print("Ошибка при получении курсов студента: ", error)
        return []

def get_course_students(course_id):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''
            SELECT students.* FROM students
            JOIN student_courses ON students.id = student_courses.student_id
            WHERE student_courses.course_id = ?
            ''', (course_id,))
            return [dict(row) for row in c.fetchall()]
    except sqlite3.Error as error:
        print("Ошибка при получении студентов курса: ", error)

def transfer_student(student_id, new_group):
    try:
        with sqlite3.connect('university.db') as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            c = conn.cursor()
            c.execute('''
            SELECT group_name FROM students WHERE id = ?
            ''', (student_id,))
            row = c.fetchone()
            if not row:
                print("Студент не найден")
                return False

            c.execute('''
            UPDATE students SET group_name = ? WHERE id = ?
            ''', (new_group, student_id))

            c.execute('''
            DELETE FROM student_courses WHERE student_id = ?
            ''', (student_id,))
            return True
    except sqlite3.Error as error:
        print("Ошибка при переводе студента: ", error)
        return False

def display_all_courses():
    try:
        with sqlite3.connect('university.db') as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM courses")
            courses = [dict(row) for row in c.fetchall()]
            print("\nВсе курсы")
            print_table(courses, COURSE_FIELDS)
    except sqlite3.Error as error:
        print("Ошибка при получении всех курсов:", error)


class UniversityDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn.row_factory = sqlite3.Row
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or [])
            return True
        except sqlite3.Error as error:
            print("Ошибка: ", error)
            return False

    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or [])
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as error:
            print("Ошибка: ", error)
            return []

    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or [])
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as error:
            print("Ошибка: ", error)
            return None

    def get_student_statistics(self):
        stats = {}

        stats["total_students"] = self.fetch_one("SELECT COUNT(*) AS n FROM students")["n"]

        stats["average_grade"] = self.fetch_one("SELECT AVG(average_grade) AS avg FROM students")["avg"]

        stats["groups"] = self.fetch_all("""
            SELECT group_name, COUNT(*) AS total
            FROM students GROUP BY group_name
        """)

        return stats

    def get_top_students(self, limit=5):
        return self.fetch_all("""
            SELECT * FROM students
            ORDER BY average_grade DESC
            LIMIT ?
        """, (limit,))


def menu():
    while True:
        print("\n=== МЕНЮ ===")
        print("1. Добавить студента")
        print("2. Показать всех студентов")
        print("3. Найти студентов по группе")
        print("4. Обновить средний балл")
        print("5. Удалить студента")
        print("6. Показать все курсы")
        print("7. Добавить курс")
        print("8. Записать студента на курс")
        print("9. Показать курсы студента")
        print("10. Перевести студента в другую группу")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            first_name = input("Имя: ")
            last_name = input("Фамилия: ")
            group_name = input("Группа: ")
            year = int(input("Год поступления: "))
            grade = input("Средний балл (можно оставить пустым): ")
            grade = float(grade) if grade else None
            student_id = add_student(first_name, last_name, group_name, year, grade)
            print("Студент добавлен, ID =", student_id)

        elif choice == "2":
            students = get_all_students()
            print("\nВсе студенты")
            print_table(students, STUDENT_FIELDS)

        elif choice == "3":
            group = input("Введите группу: ")
            students = get_student_by_group(group)
            print(f"\nСтуденты группы {group}")
            print_table(students, STUDENT_FIELDS)

        elif choice == "4":
            student_id = int(input("ID студента: "))
            new_grade = float(input("Новый средний балл: "))
            if update_student_grade(student_id, new_grade):
                print("Оценка обновлена")
            else:
                print("Ошибка")

        elif choice == "5":
            student_id = int(input("ID студента: "))
            if delete_student(student_id):
                print("Студент удалён")
            else:
                print("Ошибка")

        elif choice == "6":
            display_all_courses()  # новый пункт для всех курсов

        elif choice == "7":
            name = input("Название курса: ")
            instructor = input("Преподаватель: ")
            credits = int(input("Количество кредитов: "))
            course_id = add_course(name, instructor, credits)
            print("Курс добавлен, ID =", course_id)

        elif choice == "8":
            student_id = int(input("ID студента: "))
            course_id = int(input("ID курса: "))
            if enroll_student_in_course(student_id, course_id):
                print("Студент записан на курс")
            else:
                print("Ошибка")


        elif choice == "9":
            student_id = int(input("ID студента: "))
            student_list = [s for s in get_all_students() if s["id"] == student_id]
            if not student_list:
                print("Студент не найден")
                continue
            student = student_list[0]
            full_name = f'{student["first_name"]} {student["last_name"]}'
            courses = get_student_courses(student_id)
            print(f"\nКурсы студента {full_name}")
            print_table(courses, COURSE_FIELDS)


        elif choice == "10":
            student_id = int(input("ID студента: "))
            new_group = input("Новая группа: ")
            if transfer_student(student_id, new_group):
                print("Студент переведён")
            else:
                print("Ошибка")

        elif choice == "0":
            print("Выход из программы👋")
            break

        else:
            print("Неверный пункт меню")



if __name__ == '__main__':
    create_database()
    menu()
