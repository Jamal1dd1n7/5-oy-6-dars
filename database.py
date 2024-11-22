import psycopg2

class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database='postgres',
            user='postgres',
            host='localhost',
            password='252208'
        )
        self.table_names = []

    def manager(self, sql, *args, commit=False, fetchone=False, fetchall=False):
        result = None
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
        return result

    def create_students(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS students(
                student_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                student_name VARCHAR(50) NOT NULL,
                age INTEGER CHECK(age > 0),
                email VARCHAR(255) UNIQUE NOT NULL
            )
        '''
        self.manager(sql, commit=True)

    def create_courses(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS courses(
                course_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                course_name VARCHAR(50) UNIQUE NOT NULL,
                credits INTEGER CHECK(credits > 1 AND credits < 5)
            )
        '''
        self.manager(sql, commit=True)

    def create_enrollments(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS enrollments(
                enrollment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
                course_id INTEGER REFERENCES courses(course_id) ON DELETE SET NULL
            )
        '''
        self.manager(sql, commit=True)

    def create_teachers(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS teachers(
                teacher_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                experience_years INTEGER CHECK( experience_years >= 0)
            )
        '''
        self.manager(sql, commit=True)

    def create_assignments(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS course_assignments(
                assignment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                teacher_id INTEGER REFERENCES teachers(teacher_id) ON DELETE CASCADE,
                course_id INTEGER REFERENCES courses(course_id) ON DELETE SET NULL
            )
        '''
        self.manager(sql, commit=True)

    def insert_students(self):
        sql = '''
            INSERT INTO students(student_name, age, email) VALUES
            ('Ali', 22, 'ali@example.com'),
            ('Bobur', 24, 'bobur@example.com'),
            ('Anvar', 21, 'anvar@example.com'),
            ('Dilnoza', 20, 'dilnoza@example.com'),
            ('Farida', 19, 'farida@example.com'),
            ('Jamshid', 23, 'jamshid@example.com'),
            ('Madina', 22, 'madina@example.com');
        '''
        self.manager(sql, commit=True)

    def insert_courses(self):
        sql = '''
            INSERT INTO courses(course_name, credits) VALUES
            ('Python Programming', 3),
            ('Data Science', 4),
            ('Web Development', 3);
        '''
        self.manager(sql, commit=True)

    def insert_teachers(self):
        sql = '''
            INSERT INTO teachers( name, experience_years) VALUES
            ('Olimjon', 10),
            ('Nazira', 5)
        '''    
        self.manager(sql, commit=True)

    def insert_assignments(self):
        sql = '''
            INSERT INTO course_assignments( teacher_id, course_id) VALUES
            (1, 1),
            (2, 2),
            (1, 3);
        '''
        self.manager(sql, commit=True)

    def set_students(self):
        sql = '''
            ALTER TABLE students RENAME TO learners;

            ALTER TABLE learners RENAME COLUMN student_name TO full_name;
        '''
        self.manager(sql, commit=True)

    def set_students_age(self):
        sql = '''
            UPDATE learners SET age = 25 WHERE student_id = 1;
            UPDATE learners SET age = 26 WHERE student_id = 2;
        '''
        self.manager(sql, commit=True)

    def del_in_students(self):
        sql = '''
            DELETE FROM learners WHERE student_id = 3;
            DELETE FROM learners WHERE student_id = 4;
        '''
        self.manager(sql, commit=True)
    # def insert_data(self):
    #     # Students
    #     students = [
    #         ("Ali", 22, "ali@example.com"),
    #         ("Bobur", 24, "bobur@example.com"),
    #         ("Anvar", 21, "anvar@example.com"),
    #         ("Dilnoza", 20, "dilnoza@example.com"),
    #         ("Farida", 19, "farida@example.com"),
    #         ("Jamshid", 23, "jamshid@example.com"),
    #         ("Madina", 22, "madina@example.com")
    #     ]
    #     for student in students:
    #         self.manager("INSERT INTO students (student_name, age, email) VALUES (%s, %s, %s)", *student, commit=True)

    #     # Courses
    #     courses = [
    #         ("Python Programming", 3),
    #         ("Data Science", 4),
    #         ("Web Development", 3)
    #     ]
    #     for course in courses:
    #         self.manager("INSERT INTO courses (course_name, credits) VALUES (%s, %s)", *course, commit=True)

    #     # Teachers
    #     teachers = [
    #         ("Olimjon", 10),
    #         ("Nazira", 5)
    #     ]
    #     for teacher in teachers:
    #         self.manager("INSERT INTO teachers (name, experience_years) VALUES (%s, %s)", *teacher, commit=True)

    #     # Course Assignments
    #     assignments = [
    #         (1, 1),  # Teacher 1 teaches Course 1
    #         (2, 2)   # Teacher 2 teaches Course 2
    #     ]
    #     for assignment in assignments:
    #         self.manager("INSERT INTO course_assignments (teacher_id, course_id) VALUES (%s, %s)", *assignment, commit=True)
