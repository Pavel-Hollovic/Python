import mysql.connector
import pandas as pd



class Data():

    db = mysql.connector.connect(user='test', password='test', host='localhost', database='WebSysDev',
                                 port=8889)

    def students(self):
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM students")

        result = cursor.fetchall()

        df = pd.DataFrame(result)
        df.columns= ["ID", "Full Name", "Major", "Age", "Working", "Native"]
        df.set_index('ID')

        return df

    def courses(self):
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM courses")

        result = cursor.fetchall()

        df = pd.DataFrame(result)
        df.columns= ["ID", "Title", "Liberal Studies", "Credits"]
        df.set_index('ID')

        return df

    def grades(self):
        cursor = self.db.cursor()

        cursor.execute("SELECT st.fullName, st.id, cs.title, cs.id, gr.grade  FROM grades gr LEFT JOIN students st ON st.id = gr.studentId LEFT JOIN courses cs ON cs.id = gr.courseId")

        result = cursor.fetchall()

        df = pd.DataFrame(result)
        df.columns= ["Full Name", "Student ID", "Course", "Course ID", "Grade"]

        return df

    def addStudent(self, name, major, age, working, native):
        cursor = self.db.cursor()
        sql = "INSERT INTO students(fullName, major, age, working, native) VALUES (%s, %s, %s, %s, %s)"
        data = (name, major, age, working, native)
        cursor.execute(sql, data)
        self.db.commit()

    def addCourse(self, title, liberal, credits):
        cursor = self.db.cursor()
        sql = "INSERT INTO courses(title, liberalStudies, credits) VALUES (%s, %s, %s)"
        data = (title, liberal, credits)
        cursor.execute(sql, data)
        self.db.commit()

    def enrolStudent(self, studentId, courseId):
        cursor = self.db.cursor()
        sql = "INSERT INTO grades(studentId, courseId) VALUES (%s, %s)"
        data = (studentId, courseId)
        cursor.execute(sql, data)
        self.db.commit()

    def gradeStudent(self, grade, studentId, courseId):
        cursor = self.db.cursor()
        sql = ("UPDATE grades SET grade = %s WHERE studentId = %s AND courseId = %s")
        data = (grade, studentId, courseId)
        cursor.execute(sql, data)
        self.db.commit()

    def csvExport(self,df):
        df.to_csv(r'/Users/pavelhollovic/Desktop/export_dataframe.csv', index=False, header=True)







class Ui():
    def menu(self):
        print ("MENU: Write number of your choosing")
        print ("1 for Students")
        print ("2 for Courses")
        print ("3 for Students Grades")
        print ("4 for Adding Student")
        print ("5 for Adding Course")
        print ("6 for Enrol Student (you will need StudentID and CourseID)")
        print ("7 for Grading Student (you will need StudentID and CourseID)")
        while True:
            try:
                return int(input())
            except:
                continue

    def display(self, data: Data, df):
        print(df)
        print("If you want to (e)xport write e or anything else to continue")
        while True:
            try:
                if "e" == input():
                    data.csvExport(df)
                    print("Export Successful you can find the file on your desktop")
                    break
            except:
                print("No export needed!")
                break



    def wait(self):
        print("Write c to (c)ontinue")
        while True:
            try:
                if "c" == input():
                    break
            except:
                print("Wrong value")
                continue

    def addStudent(self, data: Data):
        while True:
            try:
                name = input("Name: ")
                major = input("Major: ")
                age = int(input("Age: "))
                working = int(input("Working (wirte 0 for NO or 1 for YES): "))
                native = int(input("Native (wirte 0 for NO or 1 for YES): "))
                data.addStudent(name, major, age, working, native)
                break
            except (ValueError):
                print("Wrong value")
                continue
    def addCourse(self, data: Data):
        while True:
            try:
                title = input("Name: ")
                liberal = int(input("Liberal Studies (wirte 0 for NO or 1 for YES): "))
                credits = int(input("Credits: "))
                data.addCourse(title, liberal, credits)
                break
            except (ValueError):
                print("Wrong value")
                continue

    def enrolStudent(self, data: Data):
        while True:
            try:
                studentId = int(input("Student ID: "))
                courseId = int(input("Course ID: "))
                data.enrolStudent(studentId, courseId)
                break
            except (ValueError):
                print("Wrong value")
                continue

    def gradeStudent(self, data: Data):
        while True:
            try:
                grade = int(input("Grade: "))
                studentId = int(input("Student ID: "))
                courseId = int(input("Course ID: "))
                data.gradeStudent(grade, studentId, courseId)
                break
            except (ValueError):
                print("Wrong value")
                continue


class Application():
    def __init__(self):
        self.data: Data = Data()
        self.ui: Ui = Ui()

    def start(self):
        print("Hello! welcome to the Grading application.")
        while True:
            command = self.ui.menu()
            if command == 1:
                self.ui.display(self.data, self.data.students())
            elif command == 2:
                self.ui.display(self.data, self.data.courses())
            elif command == 3:
                self.ui.display(self.data, self.data.grades())
            elif command == 4:
                self.ui.addStudent(self.data)
            elif command == 5:
                self.ui.addCourse(self.data)
            elif command == 6:
                self.ui.enrolStudent(self.data)
            elif command == 7:
                self.ui.gradeStudent(self.data)
            self.ui.wait()



application = Application()
application.start()








