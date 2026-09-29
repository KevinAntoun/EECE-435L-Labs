import sys
import csv

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QMessageBox,
    QFileDialog,
    QLabel,
    QInputDialog,
    QAbstractItemView
)

from part1 import Student, Instructor, Course, save_data, load_data


class SchoolManagementApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("School Management System")
        self.resize(1100, 700)

        # Store all objects
        self.students = []
        self.instructors = []
        self.courses = []

        self.create_gui()


    # =====================================================
    # MAIN GUI
    # =====================================================

    def create_gui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        title = QLabel("School Management System")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        main_layout.addWidget(title)

        self.tabs = QTabWidget()

        main_layout.addWidget(self.tabs)

        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()
        self.registration_tab = QWidget()
        self.records_tab = QWidget()

        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.instructor_tab, "Instructors")
        self.tabs.addTab(self.course_tab, "Courses")
        self.tabs.addTab(
            self.registration_tab,
            "Registration / Assignment"
        )
        self.tabs.addTab(self.records_tab, "Records")

        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_registration_tab()
        self.create_records_tab()


    # =====================================================
    # STUDENT FORM
    # =====================================================

    def create_student_tab(self):

        layout = QFormLayout()

        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()

        layout.addRow("Name:", self.student_name)
        layout.addRow("Age:", self.student_age)
        layout.addRow("Email:", self.student_email)
        layout.addRow("Student ID:", self.student_id)

        button = QPushButton("Add Student")
        button.clicked.connect(self.add_student)

        layout.addRow(button)

        self.student_tab.setLayout(layout)


    # =====================================================
    # INSTRUCTOR FORM
    # =====================================================

    def create_instructor_tab(self):

        layout = QFormLayout()

        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()

        layout.addRow("Name:", self.instructor_name)
        layout.addRow("Age:", self.instructor_age)
        layout.addRow("Email:", self.instructor_email)
        layout.addRow("Instructor ID:", self.instructor_id)

        button = QPushButton("Add Instructor")
        button.clicked.connect(self.add_instructor)

        layout.addRow(button)

        self.instructor_tab.setLayout(layout)


    # =====================================================
    # COURSE FORM
    # =====================================================

    def create_course_tab(self):

        layout = QFormLayout()

        self.course_id = QLineEdit()
        self.course_name = QLineEdit()

        layout.addRow("Course ID:", self.course_id)
        layout.addRow("Course Name:", self.course_name)

        button = QPushButton("Add Course")
        button.clicked.connect(self.add_course)

        layout.addRow(button)

        self.course_tab.setLayout(layout)


    # =====================================================
    # REGISTRATION / ASSIGNMENT
    # =====================================================

    def create_registration_tab(self):

        main_layout = QVBoxLayout()


        # Student registration
        student_layout = QHBoxLayout()

        student_layout.addWidget(QLabel("Student:"))

        self.student_combo = QComboBox()
        student_layout.addWidget(self.student_combo)

        student_layout.addWidget(QLabel("Course:"))

        self.student_course_combo = QComboBox()
        student_layout.addWidget(self.student_course_combo)

        register_button = QPushButton("Register Student")
        register_button.clicked.connect(self.register_student)

        student_layout.addWidget(register_button)

        main_layout.addLayout(student_layout)


        # Instructor assignment
        instructor_layout = QHBoxLayout()

        instructor_layout.addWidget(QLabel("Instructor:"))

        self.instructor_combo = QComboBox()
        instructor_layout.addWidget(self.instructor_combo)

        instructor_layout.addWidget(QLabel("Course:"))

        self.instructor_course_combo = QComboBox()
        instructor_layout.addWidget(
            self.instructor_course_combo
        )

        assign_button = QPushButton("Assign Instructor")
        assign_button.clicked.connect(self.assign_instructor)

        instructor_layout.addWidget(assign_button)

        main_layout.addLayout(instructor_layout)

        self.registration_tab.setLayout(main_layout)


    # =====================================================
    # RECORDS
    # =====================================================

    def create_records_tab(self):

        layout = QVBoxLayout()


        # Search section
        search_layout = QHBoxLayout()

        search_layout.addWidget(QLabel("Search:"))

        self.search_box = QLineEdit()

        search_layout.addWidget(self.search_box)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)

        search_layout.addWidget(search_button)

        show_all_button = QPushButton("Show All")
        show_all_button.clicked.connect(self.refresh_table)

        search_layout.addWidget(show_all_button)

        layout.addLayout(search_layout)


        # Table
        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "Type",
                "ID",
                "Name",
                "Age",
                "Email",
                "Details"
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        layout.addWidget(self.table)


        # Buttons
        button_layout = QHBoxLayout()

        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_record)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_record)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_file)

        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_file)

        export_button = QPushButton("Export CSV")
        export_button.clicked.connect(self.export_csv)

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(load_button)
        button_layout.addWidget(export_button)

        layout.addLayout(button_layout)

        self.records_tab.setLayout(layout)


    # =====================================================
    # ADD STUDENT
    # =====================================================

    def add_student(self):

        try:

            name = self.student_name.text().strip()
            age_text = self.student_age.text().strip()
            email = self.student_email.text().strip()
            student_id = self.student_id.text().strip()

            if not name:
                raise ValueError("Student name cannot be empty.")

            if not student_id:
                raise ValueError("Student ID cannot be empty.")

            if not age_text:
                raise ValueError("Age cannot be empty.")

            age = int(age_text)

            # Duplicate ID check
            for student in self.students:

                if student.student_id == student_id:
                    raise ValueError(
                        "Student ID already exists."
                    )

            student = Student(
                name,
                age,
                email,
                student_id
            )

            self.students.append(student)

            QMessageBox.information(
                self,
                "Success",
                "Student added successfully."
            )

            self.student_name.clear()
            self.student_age.clear()
            self.student_email.clear()
            self.student_id.clear()

            self.refresh_all()

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )


    # =====================================================
    # ADD INSTRUCTOR
    # =====================================================

    def add_instructor(self):

        try:

            name = self.instructor_name.text().strip()
            age_text = self.instructor_age.text().strip()
            email = self.instructor_email.text().strip()
            instructor_id = self.instructor_id.text().strip()

            if not name:
                raise ValueError(
                    "Instructor name cannot be empty."
                )

            if not instructor_id:
                raise ValueError(
                    "Instructor ID cannot be empty."
                )

            if not age_text:
                raise ValueError("Age cannot be empty.")

            age = int(age_text)

            for instructor in self.instructors:

                if instructor.instructor_id == instructor_id:
                    raise ValueError(
                        "Instructor ID already exists."
                    )

            instructor = Instructor(
                name,
                age,
                email,
                instructor_id
            )

            self.instructors.append(instructor)

            QMessageBox.information(
                self,
                "Success",
                "Instructor added successfully."
            )

            self.instructor_name.clear()
            self.instructor_age.clear()
            self.instructor_email.clear()
            self.instructor_id.clear()

            self.refresh_all()

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )


    # =====================================================
    # ADD COURSE
    # =====================================================

    def add_course(self):

        try:

            course_id = self.course_id.text().strip()
            course_name = self.course_name.text().strip()

            if not course_id:
                raise ValueError(
                    "Course ID cannot be empty."
                )

            if not course_name:
                raise ValueError(
                    "Course name cannot be empty."
                )

            for course in self.courses:

                if course.course_id == course_id:
                    raise ValueError(
                        "Course ID already exists."
                    )

            course = Course(
                course_id,
                course_name
            )

            self.courses.append(course)

            QMessageBox.information(
                self,
                "Success",
                "Course added successfully."
            )

            self.course_id.clear()
            self.course_name.clear()

            self.refresh_all()

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )


    # =====================================================
    # STUDENT REGISTRATION
    # =====================================================

    def register_student(self):

        if (
            self.student_combo.currentIndex() == -1
            or self.student_course_combo.currentIndex() == -1
        ):

            QMessageBox.warning(
                self,
                "Error",
                "Select a student and course."
            )

            return

        student_id = self.student_combo.currentData()

        course_id = self.student_course_combo.currentData()

        student = self.find_student(student_id)
        course = self.find_course(course_id)

        if course in student.registered_courses:

            QMessageBox.warning(
                self,
                "Warning",
                "Student is already registered in this course."
            )

            return

        student.register_course(course)

        QMessageBox.information(
            self,
            "Success",
            f"{student.name} registered in "
            f"{course.course_name}."
        )

        self.refresh_table()


    # =====================================================
    # INSTRUCTOR ASSIGNMENT
    # =====================================================

    def assign_instructor(self):

        if (
            self.instructor_combo.currentIndex() == -1
            or self.instructor_course_combo.currentIndex() == -1
        ):

            QMessageBox.warning(
                self,
                "Error",
                "Select an instructor and course."
            )

            return

        instructor_id = self.instructor_combo.currentData()

        course_id = self.instructor_course_combo.currentData()

        instructor = self.find_instructor(instructor_id)
        course = self.find_course(course_id)


        # If course already has another instructor
        if course.instructor is not None:

            old_instructor = course.instructor

            if course in old_instructor.assigned_courses:
                old_instructor.assigned_courses.remove(course)


        instructor.assign_course(course)

        QMessageBox.information(
            self,
            "Success",
            f"{instructor.name} assigned to "
            f"{course.course_name}."
        )

        self.refresh_table()


    # =====================================================
    # FIND OBJECTS
    # =====================================================

    def find_student(self, student_id):

        for student in self.students:

            if student.student_id == student_id:
                return student

        return None


    def find_instructor(self, instructor_id):

        for instructor in self.instructors:

            if instructor.instructor_id == instructor_id:
                return instructor

        return None


    def find_course(self, course_id):

        for course in self.courses:

            if course.course_id == course_id:
                return course

        return None


    # =====================================================
    # DROPDOWNS
    # =====================================================

    def refresh_dropdowns(self):

        self.student_combo.clear()
        self.instructor_combo.clear()
        self.student_course_combo.clear()
        self.instructor_course_combo.clear()


        for student in self.students:

            self.student_combo.addItem(
                f"{student.student_id} - {student.name}",
                student.student_id
            )


        for instructor in self.instructors:

            self.instructor_combo.addItem(
                f"{instructor.instructor_id} - "
                f"{instructor.name}",
                instructor.instructor_id
            )


        for course in self.courses:

            text = (
                f"{course.course_id} - "
                f"{course.course_name}"
            )

            self.student_course_combo.addItem(
                text,
                course.course_id
            )

            self.instructor_course_combo.addItem(
                text,
                course.course_id
            )


    # =====================================================
    # DISPLAY TABLE
    # =====================================================

    def refresh_table(self):

        self.table.setRowCount(0)


        # Students
        for student in self.students:

            courses = ", ".join(
                course.course_name
                for course in student.registered_courses
            )

            self.add_table_row(
                "Student",
                student.student_id,
                student.name,
                student.age,
                student.email,
                courses
            )


        # Instructors
        for instructor in self.instructors:

            courses = ", ".join(
                course.course_name
                for course in instructor.assigned_courses
            )

            self.add_table_row(
                "Instructor",
                instructor.instructor_id,
                instructor.name,
                instructor.age,
                instructor.email,
                courses
            )


        # Courses
        for course in self.courses:

            if course.instructor:
                instructor_name = course.instructor.name
            else:
                instructor_name = "None"

            student_names = ", ".join(
                student.name
                for student in course.enrolled_students
            )

            details = (
                f"Instructor: {instructor_name}; "
                f"Students: {student_names}"
            )

            self.add_table_row(
                "Course",
                course.course_id,
                course.course_name,
                "",
                "",
                details
            )

        self.table.resizeColumnsToContents()


    def add_table_row(
        self,
        record_type,
        record_id,
        name,
        age,
        email,
        details
    ):

        row = self.table.rowCount()

        self.table.insertRow(row)

        values = [
            record_type,
            record_id,
            name,
            age,
            email,
            details
        ]

        for column, value in enumerate(values):

            item = QTableWidgetItem(str(value))

            self.table.setItem(
                row,
                column,
                item
            )


    # =====================================================
    # SEARCH
    # =====================================================

    def search_records(self):

        query = self.search_box.text().strip().lower()

        if not query:

            self.refresh_table()
            return


        self.table.setRowCount(0)


        # Students
        for student in self.students:

            course_text = " ".join(
                f"{course.course_id} {course.course_name}"
                for course in student.registered_courses
            )

            search_text = (
                f"{student.name} "
                f"{student.student_id} "
                f"{student.email} "
                f"{course_text}"
            ).lower()

            if query in search_text:

                self.add_table_row(
                    "Student",
                    student.student_id,
                    student.name,
                    student.age,
                    student.email,
                    course_text
                )


        # Instructors
        for instructor in self.instructors:

            course_text = " ".join(
                f"{course.course_id} {course.course_name}"
                for course in instructor.assigned_courses
            )

            search_text = (
                f"{instructor.name} "
                f"{instructor.instructor_id} "
                f"{instructor.email} "
                f"{course_text}"
            ).lower()

            if query in search_text:

                self.add_table_row(
                    "Instructor",
                    instructor.instructor_id,
                    instructor.name,
                    instructor.age,
                    instructor.email,
                    course_text
                )


        # Courses
        for course in self.courses:

            instructor_name = (
                course.instructor.name
                if course.instructor
                else ""
            )

            student_names = " ".join(
                student.name
                for student in course.enrolled_students
            )

            search_text = (
                f"{course.course_id} "
                f"{course.course_name} "
                f"{instructor_name} "
                f"{student_names}"
            ).lower()

            if query in search_text:

                self.add_table_row(
                    "Course",
                    course.course_id,
                    course.course_name,
                    "",
                    "",
                    f"Instructor: {instructor_name}; "
                    f"Students: {student_names}"
                )


    # =====================================================
    # EDIT RECORD
    # =====================================================

    def edit_record(self):

        row = self.table.currentRow()

        if row == -1:

            QMessageBox.warning(
                self,
                "Warning",
                "Select a record first."
            )

            return


        record_type = self.table.item(row, 0).text()
        record_id = self.table.item(row, 1).text()


        try:

            # STUDENT
            if record_type == "Student":

                student = self.find_student(record_id)

                name, ok = QInputDialog.getText(
                    self,
                    "Edit Student",
                    "Name:",
                    text=student.name
                )

                if not ok:
                    return

                age, ok = QInputDialog.getInt(
                    self,
                    "Edit Student",
                    "Age:",
                    student.age,
                    0
                )

                if not ok:
                    return

                email, ok = QInputDialog.getText(
                    self,
                    "Edit Student",
                    "Email:",
                    text=student.email
                )

                if not ok:
                    return

                student.name = name
                student.age = age
                student.email = email


            # INSTRUCTOR
            elif record_type == "Instructor":

                instructor = self.find_instructor(record_id)

                name, ok = QInputDialog.getText(
                    self,
                    "Edit Instructor",
                    "Name:",
                    text=instructor.name
                )

                if not ok:
                    return

                age, ok = QInputDialog.getInt(
                    self,
                    "Edit Instructor",
                    "Age:",
                    instructor.age,
                    0
                )

                if not ok:
                    return

                email, ok = QInputDialog.getText(
                    self,
                    "Edit Instructor",
                    "Email:",
                    text=instructor.email
                )

                if not ok:
                    return

                instructor.name = name
                instructor.age = age
                instructor.email = email


            # COURSE
            elif record_type == "Course":

                course = self.find_course(record_id)

                name, ok = QInputDialog.getText(
                    self,
                    "Edit Course",
                    "Course Name:",
                    text=course.course_name
                )

                if not ok:
                    return

                course.course_name = name


            self.refresh_all()

            QMessageBox.information(
                self,
                "Success",
                "Record updated successfully."
            )


        except ValueError as error:

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )


    # =====================================================
    # DELETE RECORD
    # =====================================================

    def delete_record(self):

        row = self.table.currentRow()

        if row == -1:

            QMessageBox.warning(
                self,
                "Warning",
                "Select a record first."
            )

            return


        record_type = self.table.item(row, 0).text()
        record_id = self.table.item(row, 1).text()


        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this record?",
            QMessageBox.Yes | QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return


        # DELETE STUDENT
        if record_type == "Student":

            student = self.find_student(record_id)

            if student:

                for course in student.registered_courses:

                    if student in course.enrolled_students:
                        course.enrolled_students.remove(student)

                self.students.remove(student)


        # DELETE INSTRUCTOR
        elif record_type == "Instructor":

            instructor = self.find_instructor(record_id)

            if instructor:

                for course in instructor.assigned_courses:

                    if course.instructor == instructor:
                        course.instructor = None

                self.instructors.remove(instructor)


        # DELETE COURSE
        elif record_type == "Course":

            course = self.find_course(record_id)

            if course:

                for student in course.enrolled_students:

                    if course in student.registered_courses:
                        student.registered_courses.remove(course)

                if course.instructor:

                    if course in course.instructor.assigned_courses:
                        course.instructor.assigned_courses.remove(course)

                self.courses.remove(course)


        self.refresh_all()

        QMessageBox.information(
            self,
            "Success",
            "Record deleted successfully."
        )


    # =====================================================
    # SAVE JSON
    # =====================================================

    def save_file(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Data",
            "",
            "JSON Files (*.json)"
        )

        if not filename:
            return

        if not filename.endswith(".json"):
            filename += ".json"

        try:

            save_data(
                self.students,
                self.instructors,
                self.courses,
                filename
            )

            QMessageBox.information(
                self,
                "Success",
                "Data saved successfully."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )


    # =====================================================
    # LOAD JSON
    # =====================================================

    def load_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Data",
            "",
            "JSON Files (*.json)"
        )

        if not filename:
            return


        try:

            (
                self.students,
                self.instructors,
                self.courses
            ) = load_data(filename)

            self.refresh_all()

            QMessageBox.information(
                self,
                "Success",
                "Data loaded successfully."
            )


        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )


    # =====================================================
    # EXPORT CSV
    # =====================================================

    def export_csv(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            "",
            "CSV Files (*.csv)"
        )

        if not filename:
            return

        if not filename.endswith(".csv"):
            filename += ".csv"


        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    [
                        "Type",
                        "ID",
                        "Name",
                        "Age",
                        "Email",
                        "Details"
                    ]
                )


                # Students
                for student in self.students:

                    courses = ", ".join(
                        course.course_name
                        for course
                        in student.registered_courses
                    )

                    writer.writerow(
                        [
                            "Student",
                            student.student_id,
                            student.name,
                            student.age,
                            student.email,
                            courses
                        ]
                    )


                # Instructors
                for instructor in self.instructors:

                    courses = ", ".join(
                        course.course_name
                        for course
                        in instructor.assigned_courses
                    )

                    writer.writerow(
                        [
                            "Instructor",
                            instructor.instructor_id,
                            instructor.name,
                            instructor.age,
                            instructor.email,
                            courses
                        ]
                    )


                # Courses
                for course in self.courses:

                    instructor_name = (
                        course.instructor.name
                        if course.instructor
                        else "None"
                    )

                    students = ", ".join(
                        student.name
                        for student
                        in course.enrolled_students
                    )

                    writer.writerow(
                        [
                            "Course",
                            course.course_id,
                            course.course_name,
                            "",
                            "",
                            f"Instructor: "
                            f"{instructor_name}; "
                            f"Students: {students}"
                        ]
                    )


            QMessageBox.information(
                self,
                "Success",
                "Data exported to CSV successfully."
            )


        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )


    # =====================================================
    # REFRESH EVERYTHING
    # =====================================================

    def refresh_all(self):

        self.refresh_dropdowns()
        self.refresh_table()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SchoolManagementApp()

    window.show()

    sys.exit(app.exec_())