import sys
import re
import sqlite3
import shutil

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


# =========================================================
# DATABASE
# =========================================================

class DatabaseManager:

    def __init__(self, database_name="school.db"):
        self.database_name = database_name

        self.connection = sqlite3.connect(database_name)

        # Enable foreign keys
        self.connection.execute("PRAGMA foreign_keys = ON")

        self.create_tables()


    # -----------------------------------------------------
    # CREATE DATABASE TABLES
    # -----------------------------------------------------

    def create_tables(self):

        cursor = self.connection.cursor()

        # Students
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age >= 0),
                email TEXT NOT NULL
            )
        """)

        # Instructors
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS instructors (
                instructor_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age >= 0),
                email TEXT NOT NULL
            )
        """)

        # Courses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL,
                instructor_id TEXT,

                FOREIGN KEY (instructor_id)
                    REFERENCES instructors(instructor_id)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            )
        """)

        # Enrollments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                student_id TEXT,
                course_id TEXT,

                PRIMARY KEY (student_id, course_id),

                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE,

                FOREIGN KEY (course_id)
                    REFERENCES courses(course_id)
                    ON DELETE CASCADE
            )
        """)

        self.connection.commit()


    # =====================================================
    # STUDENT CRUD
    # =====================================================

    def add_student(self, student_id, name, age, email):

        with self.connection:

            self.connection.execute("""
                INSERT INTO students
                (student_id, name, age, email)
                VALUES (?, ?, ?, ?)
            """, (
                student_id,
                name,
                age,
                email
            ))


    def get_students(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT student_id, name, age, email
            FROM students
            ORDER BY name
        """)

        return cursor.fetchall()


    def update_student(self, student_id, name, age, email):

        with self.connection:

            self.connection.execute("""
                UPDATE students
                SET name = ?,
                    age = ?,
                    email = ?
                WHERE student_id = ?
            """, (
                name,
                age,
                email,
                student_id
            ))


    def delete_student(self, student_id):

        with self.connection:

            self.connection.execute("""
                DELETE FROM students
                WHERE student_id = ?
            """, (student_id,))


    # =====================================================
    # INSTRUCTOR CRUD
    # =====================================================

    def add_instructor(
        self,
        instructor_id,
        name,
        age,
        email
    ):

        with self.connection:

            self.connection.execute("""
                INSERT INTO instructors
                (instructor_id, name, age, email)
                VALUES (?, ?, ?, ?)
            """, (
                instructor_id,
                name,
                age,
                email
            ))


    def get_instructors(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT instructor_id, name, age, email
            FROM instructors
            ORDER BY name
        """)

        return cursor.fetchall()


    def update_instructor(
        self,
        instructor_id,
        name,
        age,
        email
    ):

        with self.connection:

            self.connection.execute("""
                UPDATE instructors
                SET name = ?,
                    age = ?,
                    email = ?
                WHERE instructor_id = ?
            """, (
                name,
                age,
                email,
                instructor_id
            ))


    def delete_instructor(self, instructor_id):

        with self.connection:

            self.connection.execute("""
                DELETE FROM instructors
                WHERE instructor_id = ?
            """, (instructor_id,))


    # =====================================================
    # COURSE CRUD
    # =====================================================

    def add_course(self, course_id, course_name):

        with self.connection:

            self.connection.execute("""
                INSERT INTO courses
                (course_id, course_name)
                VALUES (?, ?)
            """, (
                course_id,
                course_name
            ))


    def get_courses(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT course_id, course_name
            FROM courses
            ORDER BY course_name
        """)

        return cursor.fetchall()


    def update_course(self, course_id, course_name):

        with self.connection:

            self.connection.execute("""
                UPDATE courses
                SET course_name = ?
                WHERE course_id = ?
            """, (
                course_name,
                course_id
            ))


    def delete_course(self, course_id):

        with self.connection:

            self.connection.execute("""
                DELETE FROM courses
                WHERE course_id = ?
            """, (course_id,))


    # =====================================================
    # ENROLLMENT
    # =====================================================

    def enroll_student(self, student_id, course_id):

        with self.connection:

            self.connection.execute("""
                INSERT INTO enrollments
                (student_id, course_id)
                VALUES (?, ?)
            """, (
                student_id,
                course_id
            ))


    def remove_enrollment(self, student_id, course_id):

        with self.connection:

            self.connection.execute("""
                DELETE FROM enrollments
                WHERE student_id = ?
                AND course_id = ?
            """, (
                student_id,
                course_id
            ))


    # =====================================================
    # ASSIGN INSTRUCTOR
    # =====================================================

    def assign_instructor(
        self,
        instructor_id,
        course_id
    ):

        with self.connection:

            self.connection.execute("""
                UPDATE courses
                SET instructor_id = ?
                WHERE course_id = ?
            """, (
                instructor_id,
                course_id
            ))


    # =====================================================
    # DISPLAY ALL RECORDS
    # =====================================================

    def get_all_records(self, search=""):

        records = []

        cursor = self.connection.cursor()


        # STUDENTS
        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                s.age,
                s.email,
                COALESCE(
                    GROUP_CONCAT(c.course_name, ', '),
                    ''
                )

            FROM students s

            LEFT JOIN enrollments e
                ON s.student_id = e.student_id

            LEFT JOIN courses c
                ON e.course_id = c.course_id

            GROUP BY
                s.student_id,
                s.name,
                s.age,
                s.email
        """)

        for row in cursor.fetchall():

            records.append((
                "Student",
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            ))


        # INSTRUCTORS
        cursor.execute("""
            SELECT
                i.instructor_id,
                i.name,
                i.age,
                i.email,
                COALESCE(
                    GROUP_CONCAT(c.course_name, ', '),
                    ''
                )

            FROM instructors i

            LEFT JOIN courses c
                ON i.instructor_id = c.instructor_id

            GROUP BY
                i.instructor_id,
                i.name,
                i.age,
                i.email
        """)

        for row in cursor.fetchall():

            records.append((
                "Instructor",
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            ))


        # COURSES
        cursor.execute("""
            SELECT
                c.course_id,
                c.course_name,
                COALESCE(i.name, 'None'),
                COALESCE(
                    GROUP_CONCAT(s.name, ', '),
                    ''
                )

            FROM courses c

            LEFT JOIN instructors i
                ON c.instructor_id = i.instructor_id

            LEFT JOIN enrollments e
                ON c.course_id = e.course_id

            LEFT JOIN students s
                ON e.student_id = s.student_id

            GROUP BY
                c.course_id,
                c.course_name,
                i.name
        """)

        for row in cursor.fetchall():

            details = (
                f"Instructor: {row[2]}; "
                f"Students: {row[3]}"
            )

            records.append((
                "Course",
                row[0],
                row[1],
                "",
                "",
                details
            ))


        # Search
        if search:

            search = search.lower()

            records = [
                record
                for record in records
                if search in " ".join(
                    str(value).lower()
                    for value in record
                )
            ]

        return records


    # =====================================================
    # BACKUP
    # =====================================================

    def backup_database(self, backup_filename):

        self.connection.commit()

        backup_connection = sqlite3.connect(
            backup_filename
        )

        self.connection.backup(
            backup_connection
        )

        backup_connection.close()


    # =====================================================
    # RESTORE
    # =====================================================

    def restore_database(self, backup_filename):

        self.connection.close()

        shutil.copy2(
            backup_filename,
            self.database_name
        )

        self.connection = sqlite3.connect(
            self.database_name
        )

        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )


    def close(self):

        self.connection.close()


# =========================================================
# PYQT GUI
# =========================================================

class SchoolManagementApp(QMainWindow):

    def __init__(self):

        super().__init__()

        self.db = DatabaseManager()

        self.setWindowTitle(
            "School Management System"
        )

        self.resize(1100, 700)

        self.create_gui()

        self.refresh_all()


    # =====================================================
    # GUI
    # =====================================================

    def create_gui(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout()

        central_widget.setLayout(
            main_layout
        )

        title = QLabel(
            "School Management System - SQLite"
        )

        title.setStyleSheet(
            "font-size: 22px; "
            "font-weight: bold;"
        )

        main_layout.addWidget(title)


        self.tabs = QTabWidget()

        main_layout.addWidget(self.tabs)


        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()
        self.registration_tab = QWidget()
        self.records_tab = QWidget()


        self.tabs.addTab(
            self.student_tab,
            "Students"
        )

        self.tabs.addTab(
            self.instructor_tab,
            "Instructors"
        )

        self.tabs.addTab(
            self.course_tab,
            "Courses"
        )

        self.tabs.addTab(
            self.registration_tab,
            "Registration / Assignment"
        )

        self.tabs.addTab(
            self.records_tab,
            "Records"
        )


        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_registration_tab()
        self.create_records_tab()


    # =====================================================
    # STUDENT
    # =====================================================

    def create_student_tab(self):

        layout = QFormLayout()

        self.student_id = QLineEdit()
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()

        layout.addRow(
            "Student ID:",
            self.student_id
        )

        layout.addRow(
            "Name:",
            self.student_name
        )

        layout.addRow(
            "Age:",
            self.student_age
        )

        layout.addRow(
            "Email:",
            self.student_email
        )

        button = QPushButton(
            "Add Student"
        )

        button.clicked.connect(
            self.add_student
        )

        layout.addRow(button)

        self.student_tab.setLayout(layout)


    # =====================================================
    # INSTRUCTOR
    # =====================================================

    def create_instructor_tab(self):

        layout = QFormLayout()

        self.instructor_id = QLineEdit()
        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()

        layout.addRow(
            "Instructor ID:",
            self.instructor_id
        )

        layout.addRow(
            "Name:",
            self.instructor_name
        )

        layout.addRow(
            "Age:",
            self.instructor_age
        )

        layout.addRow(
            "Email:",
            self.instructor_email
        )

        button = QPushButton(
            "Add Instructor"
        )

        button.clicked.connect(
            self.add_instructor
        )

        layout.addRow(button)

        self.instructor_tab.setLayout(layout)


    # =====================================================
    # COURSE
    # =====================================================

    def create_course_tab(self):

        layout = QFormLayout()

        self.course_id = QLineEdit()
        self.course_name = QLineEdit()

        layout.addRow(
            "Course ID:",
            self.course_id
        )

        layout.addRow(
            "Course Name:",
            self.course_name
        )

        button = QPushButton(
            "Add Course"
        )

        button.clicked.connect(
            self.add_course
        )

        layout.addRow(button)

        self.course_tab.setLayout(layout)


    # =====================================================
    # REGISTRATION
    # =====================================================

    def create_registration_tab(self):

        layout = QVBoxLayout()


        student_layout = QHBoxLayout()

        student_layout.addWidget(
            QLabel("Student:")
        )

        self.student_combo = QComboBox()

        student_layout.addWidget(
            self.student_combo
        )

        student_layout.addWidget(
            QLabel("Course:")
        )

        self.student_course_combo = QComboBox()

        student_layout.addWidget(
            self.student_course_combo
        )

        register_button = QPushButton(
            "Register Student"
        )

        register_button.clicked.connect(
            self.register_student
        )

        student_layout.addWidget(
            register_button
        )

        layout.addLayout(student_layout)


        instructor_layout = QHBoxLayout()

        instructor_layout.addWidget(
            QLabel("Instructor:")
        )

        self.instructor_combo = QComboBox()

        instructor_layout.addWidget(
            self.instructor_combo
        )

        instructor_layout.addWidget(
            QLabel("Course:")
        )

        self.instructor_course_combo = QComboBox()

        instructor_layout.addWidget(
            self.instructor_course_combo
        )

        assign_button = QPushButton(
            "Assign Instructor"
        )

        assign_button.clicked.connect(
            self.assign_instructor
        )

        instructor_layout.addWidget(
            assign_button
        )

        layout.addLayout(
            instructor_layout
        )

        self.registration_tab.setLayout(
            layout
        )


    # =====================================================
    # RECORDS
    # =====================================================

    def create_records_tab(self):

        layout = QVBoxLayout()

        search_layout = QHBoxLayout()

        search_layout.addWidget(
            QLabel("Search:")
        )

        self.search_box = QLineEdit()

        search_layout.addWidget(
            self.search_box
        )

        search_button = QPushButton(
            "Search"
        )

        search_button.clicked.connect(
            self.search_records
        )

        search_layout.addWidget(
            search_button
        )

        show_button = QPushButton(
            "Show All"
        )

        show_button.clicked.connect(
            self.refresh_table
        )

        search_layout.addWidget(
            show_button
        )

        layout.addLayout(
            search_layout
        )


        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Type",
            "ID",
            "Name",
            "Age",
            "Email",
            "Details"
        ])

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        layout.addWidget(
            self.table
        )


        buttons = QHBoxLayout()


        edit_button = QPushButton(
            "Edit Selected"
        )

        edit_button.clicked.connect(
            self.edit_record
        )


        delete_button = QPushButton(
            "Delete Selected"
        )

        delete_button.clicked.connect(
            self.delete_record
        )


        backup_button = QPushButton(
            "Backup Database"
        )

        backup_button.clicked.connect(
            self.backup_database
        )


        restore_button = QPushButton(
            "Restore Database"
        )

        restore_button.clicked.connect(
            self.restore_database
        )


        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addWidget(backup_button)
        buttons.addWidget(restore_button)

        layout.addLayout(buttons)

        self.records_tab.setLayout(
            layout
        )


    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_email(self, email):

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        return re.match(
            pattern,
            email
        ) is not None


    # =====================================================
    # ADD STUDENT
    # =====================================================

    def add_student(self):

        try:

            student_id = (
                self.student_id.text().strip()
            )

            name = (
                self.student_name.text().strip()
            )

            email = (
                self.student_email.text().strip()
            )

            if not student_id or not name:
                raise ValueError(
                    "Student ID and name are required."
                )

            age = int(
                self.student_age.text()
            )

            if age < 0:
                raise ValueError(
                    "Age cannot be negative."
                )

            if not self.validate_email(email):
                raise ValueError(
                    "Invalid email format."
                )


            self.db.add_student(
                student_id,
                name,
                age,
                email
            )


            QMessageBox.information(
                self,
                "Success",
                "Student added successfully."
            )


            self.student_id.clear()
            self.student_name.clear()
            self.student_age.clear()
            self.student_email.clear()

            self.refresh_all()


        except ValueError as error:

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )


        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                "Database Error",
                "Student ID already exists."
            )


    # =====================================================
    # ADD INSTRUCTOR
    # =====================================================

    def add_instructor(self):

        try:

            instructor_id = (
                self.instructor_id.text().strip()
            )

            name = (
                self.instructor_name.text().strip()
            )

            email = (
                self.instructor_email.text().strip()
            )

            if not instructor_id or not name:

                raise ValueError(
                    "Instructor ID and name are required."
                )

            age = int(
                self.instructor_age.text()
            )

            if age < 0:

                raise ValueError(
                    "Age cannot be negative."
                )

            if not self.validate_email(email):

                raise ValueError(
                    "Invalid email format."
                )


            self.db.add_instructor(
                instructor_id,
                name,
                age,
                email
            )


            QMessageBox.information(
                self,
                "Success",
                "Instructor added successfully."
            )


            self.instructor_id.clear()
            self.instructor_name.clear()
            self.instructor_age.clear()
            self.instructor_email.clear()

            self.refresh_all()


        except ValueError as error:

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )


        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                "Database Error",
                "Instructor ID already exists."
            )


    # =====================================================
    # ADD COURSE
    # =====================================================

    def add_course(self):

        course_id = (
            self.course_id.text().strip()
        )

        course_name = (
            self.course_name.text().strip()
        )


        if not course_id or not course_name:

            QMessageBox.warning(
                self,
                "Invalid Input",
                "Course ID and name are required."
            )

            return


        try:

            self.db.add_course(
                course_id,
                course_name
            )


            QMessageBox.information(
                self,
                "Success",
                "Course added successfully."
            )


            self.course_id.clear()
            self.course_name.clear()

            self.refresh_all()


        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                "Database Error",
                "Course ID already exists."
            )


    # =====================================================
    # REGISTER STUDENT
    # =====================================================

    def register_student(self):

        student_id = (
            self.student_combo.currentData()
        )

        course_id = (
            self.student_course_combo.currentData()
        )


        if student_id is None or course_id is None:
            return


        try:

            self.db.enroll_student(
                student_id,
                course_id
            )

            QMessageBox.information(
                self,
                "Success",
                "Student registered successfully."
            )

            self.refresh_table()


        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                "Registration Error",
                "Student is already registered "
                "in this course."
            )


    # =====================================================
    # ASSIGN INSTRUCTOR
    # =====================================================

    def assign_instructor(self):

        instructor_id = (
            self.instructor_combo.currentData()
        )

        course_id = (
            self.instructor_course_combo.currentData()
        )


        if instructor_id is None or course_id is None:
            return


        self.db.assign_instructor(
            instructor_id,
            course_id
        )


        QMessageBox.information(
            self,
            "Success",
            "Instructor assigned successfully."
        )

        self.refresh_table()


    # =====================================================
    # REFRESH DROPDOWNS
    # =====================================================

    def refresh_dropdowns(self):

        self.student_combo.clear()
        self.instructor_combo.clear()

        self.student_course_combo.clear()
        self.instructor_course_combo.clear()


        for student in self.db.get_students():

            student_id = student[0]
            name = student[1]

            self.student_combo.addItem(
                f"{student_id} - {name}",
                student_id
            )


        for instructor in self.db.get_instructors():

            instructor_id = instructor[0]
            name = instructor[1]

            self.instructor_combo.addItem(
                f"{instructor_id} - {name}",
                instructor_id
            )


        for course in self.db.get_courses():

            course_id = course[0]
            name = course[1]

            text = (
                f"{course_id} - {name}"
            )

            self.student_course_combo.addItem(
                text,
                course_id
            )

            self.instructor_course_combo.addItem(
                text,
                course_id
            )


    # =====================================================
    # TABLE
    # =====================================================

    def refresh_table(self):

        self.display_records(
            self.db.get_all_records()
        )


    def display_records(self, records):

        self.table.setRowCount(0)


        for record in records:

            row = self.table.rowCount()

            self.table.insertRow(row)

            for column, value in enumerate(record):

                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        str(value)
                    )
                )

        self.table.resizeColumnsToContents()


    # =====================================================
    # SEARCH
    # =====================================================

    def search_records(self):

        query = (
            self.search_box.text().strip()
        )

        records = self.db.get_all_records(
            query
        )

        self.display_records(records)


    # =====================================================
    # EDIT
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


        record_type = (
            self.table.item(row, 0).text()
        )

        record_id = (
            self.table.item(row, 1).text()
        )


        try:

            if record_type == "Student":

                old_name = self.table.item(
                    row, 2
                ).text()

                old_age = int(
                    self.table.item(
                        row, 3
                    ).text()
                )

                old_email = self.table.item(
                    row, 4
                ).text()


                name, ok = QInputDialog.getText(
                    self,
                    "Edit Student",
                    "Name:",
                    text=old_name
                )

                if not ok:
                    return


                age, ok = QInputDialog.getInt(
                    self,
                    "Edit Student",
                    "Age:",
                    old_age,
                    0
                )

                if not ok:
                    return


                email, ok = QInputDialog.getText(
                    self,
                    "Edit Student",
                    "Email:",
                    text=old_email
                )

                if not ok:
                    return


                if not self.validate_email(email):

                    raise ValueError(
                        "Invalid email format."
                    )


                self.db.update_student(
                    record_id,
                    name,
                    age,
                    email
                )


            elif record_type == "Instructor":

                old_name = self.table.item(
                    row, 2
                ).text()

                old_age = int(
                    self.table.item(
                        row, 3
                    ).text()
                )

                old_email = self.table.item(
                    row, 4
                ).text()


                name, ok = QInputDialog.getText(
                    self,
                    "Edit Instructor",
                    "Name:",
                    text=old_name
                )

                if not ok:
                    return


                age, ok = QInputDialog.getInt(
                    self,
                    "Edit Instructor",
                    "Age:",
                    old_age,
                    0
                )

                if not ok:
                    return


                email, ok = QInputDialog.getText(
                    self,
                    "Edit Instructor",
                    "Email:",
                    text=old_email
                )

                if not ok:
                    return


                if not self.validate_email(email):

                    raise ValueError(
                        "Invalid email format."
                    )


                self.db.update_instructor(
                    record_id,
                    name,
                    age,
                    email
                )


            elif record_type == "Course":

                old_name = self.table.item(
                    row, 2
                ).text()

                name, ok = QInputDialog.getText(
                    self,
                    "Edit Course",
                    "Course Name:",
                    text=old_name
                )

                if not ok:
                    return


                self.db.update_course(
                    record_id,
                    name
                )


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
    # DELETE
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


        record_type = (
            self.table.item(row, 0).text()
        )

        record_id = (
            self.table.item(row, 1).text()
        )


        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Delete selected record?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return


        if record_type == "Student":

            self.db.delete_student(
                record_id
            )


        elif record_type == "Instructor":

            self.db.delete_instructor(
                record_id
            )


        elif record_type == "Course":

            self.db.delete_course(
                record_id
            )


        self.refresh_all()


    # =====================================================
    # BACKUP
    # =====================================================

    def backup_database(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Backup Database",
            "",
            "SQLite Database (*.db)"
        )

        if not filename:
            return

        if not filename.endswith(".db"):
            filename += ".db"


        self.db.backup_database(
            filename
        )


        QMessageBox.information(
            self,
            "Success",
            "Database backup created."
        )


    # =====================================================
    # RESTORE
    # =====================================================

    def restore_database(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Restore Database",
            "",
            "SQLite Database (*.db)"
        )

        if not filename:
            return


        answer = QMessageBox.question(
            self,
            "Restore Database",
            "Restoring will replace the current "
            "database. Continue?",
            QMessageBox.Yes |
            QMessageBox.No
        )


        if answer != QMessageBox.Yes:
            return


        try:

            self.db.restore_database(
                filename
            )

            self.refresh_all()

            QMessageBox.information(
                self,
                "Success",
                "Database restored successfully."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Restore Error",
                str(error)
            )


    # =====================================================
    # REFRESH
    # =====================================================

    def refresh_all(self):

        self.refresh_dropdowns()
        self.refresh_table()


    # =====================================================
    # CLOSE DATABASE
    # =====================================================

    def closeEvent(self, event):

        self.db.close()

        event.accept()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SchoolManagementApp()

    window.show()

    sys.exit(app.exec_())