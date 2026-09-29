import json
import re


# -------------------------
# Person
# -------------------------
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative.")
        self._age = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not self.validate_email(value):
            raise ValueError("Invalid email format.")
        self._email = value

    @staticmethod
    def validate_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def introduce(self):
        return f"My name is {self.name} and I am {self.age} years old."


# -------------------------
# Student
# -------------------------
class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)

        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)

        if self not in course.enrolled_students:
            course.enrolled_students.append(self)


# -------------------------
# Instructor
# -------------------------
class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)

        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)

        course.instructor = self


# -------------------------
# Course
# -------------------------
class Course:
    def __init__(self, course_id, course_name, instructor=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)

        if self not in student.registered_courses:
            student.registered_courses.append(self)


# -------------------------
# Save Data
# -------------------------
def save_data(students, instructors, courses, filename="data.json"):

    data = {
        "students": [],
        "instructors": [],
        "courses": []
    }

    for student in students:
        data["students"].append({
            "name": student.name,
            "age": student.age,
            "email": student.email,
            "student_id": student.student_id,
            "registered_courses": [
                course.course_id
                for course in student.registered_courses
            ]
        })

    for instructor in instructors:
        data["instructors"].append({
            "name": instructor.name,
            "age": instructor.age,
            "email": instructor.email,
            "instructor_id": instructor.instructor_id,
            "assigned_courses": [
                course.course_id
                for course in instructor.assigned_courses
            ]
        })

    for course in courses:
        data["courses"].append({
            "course_id": course.course_id,
            "course_name": course.course_name,
            "instructor":
                course.instructor.instructor_id
                if course.instructor else None,

            "enrolled_students": [
                student.student_id
                for student in course.enrolled_students
            ]
        })

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print("Data saved successfully.")


# -------------------------
# Load Data
# -------------------------
def load_data(filename="data.json"):

    with open(filename, "r") as file:
        data = json.load(file)

    students = []
    instructors = []
    courses = []

    # Create students
    for s in data["students"]:
        student = Student(
            s["name"],
            s["age"],
            s["email"],
            s["student_id"]
        )

        students.append(student)

    # Create instructors
    for i in data["instructors"]:
        instructor = Instructor(
            i["name"],
            i["age"],
            i["email"],
            i["instructor_id"]
        )

        instructors.append(instructor)

    # Create courses
    for c in data["courses"]:
        course = Course(
            c["course_id"],
            c["course_name"]
        )

        courses.append(course)

    # Create lookup dictionaries
    student_lookup = {
        student.student_id: student
        for student in students
    }

    instructor_lookup = {
        instructor.instructor_id: instructor
        for instructor in instructors
    }

    course_lookup = {
        course.course_id: course
        for course in courses
    }

    # Restore course relationships
    for c in data["courses"]:

        course = course_lookup[c["course_id"]]

        # Restore instructor
        if c["instructor"] is not None:
            instructor = instructor_lookup[c["instructor"]]
            instructor.assign_course(course)

        # Restore students
        for student_id in c["enrolled_students"]:
            student = student_lookup[student_id]
            course.add_student(student)

    print("Data loaded successfully.")

    return students, instructors, courses