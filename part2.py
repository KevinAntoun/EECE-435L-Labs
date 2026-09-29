import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

from part1 import Student, Instructor, Course, save_data, load_data


class SchoolManagementApp:

    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("1100x700")

        # Main data lists
        self.students = []
        self.instructors = []
        self.courses = []

        self.create_gui()


    # =========================================================
    # GUI
    # =========================================================

    def create_gui(self):

        title = ttk.Label(
            self.root,
            text="School Management System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        # Notebook = tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.student_tab = ttk.Frame(notebook)
        self.instructor_tab = ttk.Frame(notebook)
        self.course_tab = ttk.Frame(notebook)
        self.relationship_tab = ttk.Frame(notebook)
        self.records_tab = ttk.Frame(notebook)

        notebook.add(self.student_tab, text="Students")
        notebook.add(self.instructor_tab, text="Instructors")
        notebook.add(self.course_tab, text="Courses")
        notebook.add(self.relationship_tab, text="Registration / Assignment")
        notebook.add(self.records_tab, text="Records")

        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_relationship_tab()
        self.create_records_tab()


    # =========================================================
    # STUDENT TAB
    # =========================================================

    def create_student_tab(self):

        frame = ttk.LabelFrame(
            self.student_tab,
            text="Add Student",
            padding=20
        )
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.student_name = ttk.Entry(frame, width=30)
        self.student_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w")
        self.student_age = ttk.Entry(frame, width=30)
        self.student_age.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w")
        self.student_email = ttk.Entry(frame, width=30)
        self.student_email.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Student ID:").grid(row=3, column=0, sticky="w")
        self.student_id = ttk.Entry(frame, width=30)
        self.student_id.grid(row=3, column=1, padx=10, pady=5)

        button = ttk.Button(
            frame,
            text="Add Student",
            command=self.add_student
        )
        button.grid(row=4, column=0, columnspan=2, pady=15)


    # =========================================================
    # INSTRUCTOR TAB
    # =========================================================

    def create_instructor_tab(self):

        frame = ttk.LabelFrame(
            self.instructor_tab,
            text="Add Instructor",
            padding=20
        )
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.instructor_name = ttk.Entry(frame, width=30)
        self.instructor_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w")
        self.instructor_age = ttk.Entry(frame, width=30)
        self.instructor_age.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w")
        self.instructor_email = ttk.Entry(frame, width=30)
        self.instructor_email.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Instructor ID:").grid(row=3, column=0, sticky="w")
        self.instructor_id = ttk.Entry(frame, width=30)
        self.instructor_id.grid(row=3, column=1, padx=10, pady=5)

        button = ttk.Button(
            frame,
            text="Add Instructor",
            command=self.add_instructor
        )
        button.grid(row=4, column=0, columnspan=2, pady=15)


    # =========================================================
    # COURSE TAB
    # =========================================================

    def create_course_tab(self):

        frame = ttk.LabelFrame(
            self.course_tab,
            text="Add Course",
            padding=20
        )
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Course ID:").grid(row=0, column=0, sticky="w")

        self.course_id = ttk.Entry(frame, width=30)
        self.course_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Course Name:").grid(row=1, column=0, sticky="w")

        self.course_name = ttk.Entry(frame, width=30)
        self.course_name.grid(row=1, column=1, padx=10, pady=5)

        button = ttk.Button(
            frame,
            text="Add Course",
            command=self.add_course
        )
        button.grid(row=2, column=0, columnspan=2, pady=15)


    # =========================================================
    # REGISTRATION / ASSIGNMENT TAB
    # =========================================================

    def create_relationship_tab(self):

        # Student registration
        student_frame = ttk.LabelFrame(
            self.relationship_tab,
            text="Register Student in Course",
            padding=20
        )
        student_frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(student_frame, text="Student:").grid(
            row=0,
            column=0,
            padx=5
        )

        self.student_combo = ttk.Combobox(
            student_frame,
            state="readonly",
            width=30
        )
        self.student_combo.grid(row=0, column=1, padx=5)

        ttk.Label(student_frame, text="Course:").grid(
            row=0,
            column=2,
            padx=5
        )

        self.student_course_combo = ttk.Combobox(
            student_frame,
            state="readonly",
            width=30
        )
        self.student_course_combo.grid(row=0, column=3, padx=5)

        ttk.Button(
            student_frame,
            text="Register",
            command=self.register_student
        ).grid(row=0, column=4, padx=10)


        # Instructor assignment
        instructor_frame = ttk.LabelFrame(
            self.relationship_tab,
            text="Assign Instructor to Course",
            padding=20
        )
        instructor_frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(instructor_frame, text="Instructor:").grid(
            row=0,
            column=0,
            padx=5
        )

        self.instructor_combo = ttk.Combobox(
            instructor_frame,
            state="readonly",
            width=30
        )
        self.instructor_combo.grid(row=0, column=1, padx=5)

        ttk.Label(instructor_frame, text="Course:").grid(
            row=0,
            column=2,
            padx=5
        )

        self.instructor_course_combo = ttk.Combobox(
            instructor_frame,
            state="readonly",
            width=30
        )
        self.instructor_course_combo.grid(row=0, column=3, padx=5)

        ttk.Button(
            instructor_frame,
            text="Assign",
            command=self.assign_instructor
        ).grid(row=0, column=4, padx=10)


    # =========================================================
    # RECORDS TAB
    # =========================================================

    def create_records_tab(self):

        search_frame = ttk.Frame(self.records_tab)
        search_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(search_frame, text="Search:").pack(side="left")

        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=10)

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_records
        ).pack(side="left")

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.refresh_tree
        ).pack(side="left", padx=5)


        columns = (
            "Type",
            "ID",
            "Name",
            "Age",
            "Email",
            "Details"
        )

        self.tree = ttk.Treeview(
            self.records_tab,
            columns=columns,
            show="headings",
            height=18
        )

        for column in columns:
            self.tree.heading(column, text=column)

        self.tree.column("Type", width=100)
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=160)
        self.tree.column("Age", width=60)
        self.tree.column("Email", width=180)
        self.tree.column("Details", width=300)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )


        button_frame = ttk.Frame(self.records_tab)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Edit Selected",
            command=self.edit_record
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_record
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Save",
            command=self.save_file
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Load",
            command=self.load_file
        ).pack(side="left", padx=5)


    # =========================================================
    # ADD OBJECTS
    # =========================================================

    def add_student(self):

        try:
            name = self.student_name.get().strip()
            age = int(self.student_age.get())
            email = self.student_email.get().strip()
            student_id = self.student_id.get().strip()

            if not name or not student_id:
                raise ValueError("Name and Student ID cannot be empty.")

            # Check duplicate ID
            for student in self.students:
                if student.student_id == student_id:
                    raise ValueError("Student ID already exists.")

            student = Student(
                name,
                age,
                email,
                student_id
            )

            self.students.append(student)

            messagebox.showinfo(
                "Success",
                "Student added successfully."
            )

            self.student_name.delete(0, tk.END)
            self.student_age.delete(0, tk.END)
            self.student_email.delete(0, tk.END)
            self.student_id.delete(0, tk.END)

            self.refresh_all()

        except ValueError as error:
            messagebox.showerror("Error", str(error))


    def add_instructor(self):

        try:
            name = self.instructor_name.get().strip()
            age = int(self.instructor_age.get())
            email = self.instructor_email.get().strip()
            instructor_id = self.instructor_id.get().strip()

            if not name or not instructor_id:
                raise ValueError("Name and Instructor ID cannot be empty.")

            for instructor in self.instructors:
                if instructor.instructor_id == instructor_id:
                    raise ValueError("Instructor ID already exists.")

            instructor = Instructor(
                name,
                age,
                email,
                instructor_id
            )

            self.instructors.append(instructor)

            messagebox.showinfo(
                "Success",
                "Instructor added successfully."
            )

            self.instructor_name.delete(0, tk.END)
            self.instructor_age.delete(0, tk.END)
            self.instructor_email.delete(0, tk.END)
            self.instructor_id.delete(0, tk.END)

            self.refresh_all()

        except ValueError as error:
            messagebox.showerror("Error", str(error))


    def add_course(self):

        try:
            course_id = self.course_id.get().strip()
            course_name = self.course_name.get().strip()

            if not course_id or not course_name:
                raise ValueError("Course ID and Course Name cannot be empty.")

            for course in self.courses:
                if course.course_id == course_id:
                    raise ValueError("Course ID already exists.")

            course = Course(
                course_id,
                course_name
            )

            self.courses.append(course)

            messagebox.showinfo(
                "Success",
                "Course added successfully."
            )

            self.course_id.delete(0, tk.END)
            self.course_name.delete(0, tk.END)

            self.refresh_all()

        except ValueError as error:
            messagebox.showerror("Error", str(error))


    # =========================================================
    # REGISTRATION
    # =========================================================

    def register_student(self):

        student_selection = self.student_combo.get()
        course_selection = self.student_course_combo.get()

        if not student_selection or not course_selection:
            messagebox.showerror(
                "Error",
                "Please select both a student and a course."
            )
            return

        student_id = student_selection.split(" - ")[0]
        course_id = course_selection.split(" - ")[0]

        student = self.find_student(student_id)
        course = self.find_course(course_id)

        if course in student.registered_courses:
            messagebox.showwarning(
                "Warning",
                "Student is already registered in this course."
            )
            return

        student.register_course(course)

        messagebox.showinfo(
            "Success",
            f"{student.name} registered in {course.course_name}."
        )

        self.refresh_tree()


    # =========================================================
    # INSTRUCTOR ASSIGNMENT
    # =========================================================

    def assign_instructor(self):

        instructor_selection = self.instructor_combo.get()
        course_selection = self.instructor_course_combo.get()

        if not instructor_selection or not course_selection:
            messagebox.showerror(
                "Error",
                "Please select an instructor and a course."
            )
            return

        instructor_id = instructor_selection.split(" - ")[0]
        course_id = course_selection.split(" - ")[0]

        instructor = self.find_instructor(instructor_id)
        course = self.find_course(course_id)

        # Remove course from previous instructor
        if course.instructor is not None:
            old_instructor = course.instructor

            if course in old_instructor.assigned_courses:
                old_instructor.assigned_courses.remove(course)

        instructor.assign_course(course)

        messagebox.showinfo(
            "Success",
            f"{instructor.name} assigned to {course.course_name}."
        )

        self.refresh_tree()


    # =========================================================
    # FIND OBJECTS
    # =========================================================

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


    # =========================================================
    # REFRESH COMBOBOXES
    # =========================================================

    def refresh_dropdowns(self):

        student_values = [
            f"{student.student_id} - {student.name}"
            for student in self.students
        ]

        instructor_values = [
            f"{instructor.instructor_id} - {instructor.name}"
            for instructor in self.instructors
        ]

        course_values = [
            f"{course.course_id} - {course.course_name}"
            for course in self.courses
        ]

        self.student_combo["values"] = student_values
        self.instructor_combo["values"] = instructor_values

        self.student_course_combo["values"] = course_values
        self.instructor_course_combo["values"] = course_values


    # =========================================================
    # DISPLAY RECORDS
    # =========================================================

    def refresh_tree(self):

        for item in self.tree.get_children():
            self.tree.delete(item)


        # Students
        for student in self.students:

            courses = ", ".join(
                course.course_name
                for course in student.registered_courses
            )

            self.tree.insert(
                "",
                tk.END,
                values=(
                    "Student",
                    student.student_id,
                    student.name,
                    student.age,
                    student.email,
                    courses
                )
            )


        # Instructors
        for instructor in self.instructors:

            courses = ", ".join(
                course.course_name
                for course in instructor.assigned_courses
            )

            self.tree.insert(
                "",
                tk.END,
                values=(
                    "Instructor",
                    instructor.instructor_id,
                    instructor.name,
                    instructor.age,
                    instructor.email,
                    courses
                )
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
                for student in course.enrolled_students
            )

            details = (
                f"Instructor: {instructor_name} | "
                f"Students: {students}"
            )

            self.tree.insert(
                "",
                tk.END,
                values=(
                    "Course",
                    course.course_id,
                    course.course_name,
                    "",
                    "",
                    details
                )
            )


    def refresh_all(self):

        self.refresh_dropdowns()
        self.refresh_tree()


    # =========================================================
    # SEARCH
    # =========================================================

    def search_records(self):

        query = self.search_entry.get().strip().lower()

        if not query:
            self.refresh_tree()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)


        # Search students
        for student in self.students:

            courses = " ".join(
                course.course_name + " " + course.course_id
                for course in student.registered_courses
            )

            searchable = (
                f"{student.name} "
                f"{student.student_id} "
                f"{student.email} "
                f"{courses}"
            ).lower()

            if query in searchable:

                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        "Student",
                        student.student_id,
                        student.name,
                        student.age,
                        student.email,
                        courses
                    )
                )


        # Search instructors
        for instructor in self.instructors:

            courses = " ".join(
                course.course_name + " " + course.course_id
                for course in instructor.assigned_courses
            )

            searchable = (
                f"{instructor.name} "
                f"{instructor.instructor_id} "
                f"{instructor.email} "
                f"{courses}"
            ).lower()

            if query in searchable:

                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        "Instructor",
                        instructor.instructor_id,
                        instructor.name,
                        instructor.age,
                        instructor.email,
                        courses
                    )
                )


        # Search courses
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

            searchable = (
                f"{course.course_id} "
                f"{course.course_name} "
                f"{instructor_name} "
                f"{student_names}"
            ).lower()

            if query in searchable:

                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        "Course",
                        course.course_id,
                        course.course_name,
                        "",
                        "",
                        f"Instructor: {instructor_name}"
                    )
                )


    # =========================================================
    # DELETE RECORD
    # =========================================================

    def delete_record(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a record first."
            )
            return

        values = self.tree.item(selected[0], "values")

        record_type = values[0]
        record_id = values[1]

        confirm = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to delete this record?"
        )

        if not confirm:
            return


        if record_type == "Student":

            student = self.find_student(record_id)

            for course in student.registered_courses:
                if student in course.enrolled_students:
                    course.enrolled_students.remove(student)

            self.students.remove(student)


        elif record_type == "Instructor":

            instructor = self.find_instructor(record_id)

            for course in instructor.assigned_courses:
                if course.instructor == instructor:
                    course.instructor = None

            self.instructors.remove(instructor)


        elif record_type == "Course":

            course = self.find_course(record_id)

            for student in course.enrolled_students:
                if course in student.registered_courses:
                    student.registered_courses.remove(course)

            if course.instructor:
                if course in course.instructor.assigned_courses:
                    course.instructor.assigned_courses.remove(course)

            self.courses.remove(course)


        self.refresh_all()

        messagebox.showinfo(
            "Success",
            "Record deleted."
        )


    # =========================================================
    # EDIT RECORD
    # =========================================================

    def edit_record(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a record first."
            )
            return

        values = self.tree.item(selected[0], "values")

        record_type = values[0]
        record_id = values[1]


        try:

            if record_type == "Student":

                student = self.find_student(record_id)

                name = simpledialog.askstring(
                    "Edit Student",
                    "Name:",
                    initialvalue=student.name
                )

                if name is None:
                    return

                age = simpledialog.askinteger(
                    "Edit Student",
                    "Age:",
                    initialvalue=student.age
                )

                if age is None:
                    return

                email = simpledialog.askstring(
                    "Edit Student",
                    "Email:",
                    initialvalue=student.email
                )

                if email is None:
                    return

                student.name = name
                student.age = age
                student.email = email


            elif record_type == "Instructor":

                instructor = self.find_instructor(record_id)

                name = simpledialog.askstring(
                    "Edit Instructor",
                    "Name:",
                    initialvalue=instructor.name
                )

                if name is None:
                    return

                age = simpledialog.askinteger(
                    "Edit Instructor",
                    "Age:",
                    initialvalue=instructor.age
                )

                if age is None:
                    return

                email = simpledialog.askstring(
                    "Edit Instructor",
                    "Email:",
                    initialvalue=instructor.email
                )

                if email is None:
                    return

                instructor.name = name
                instructor.age = age
                instructor.email = email


            elif record_type == "Course":

                course = self.find_course(record_id)

                name = simpledialog.askstring(
                    "Edit Course",
                    "Course Name:",
                    initialvalue=course.course_name
                )

                if name is None:
                    return

                course.course_name = name


            self.refresh_all()

            messagebox.showinfo(
                "Success",
                "Record updated."
            )

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )


    # =========================================================
    # SAVE
    # =========================================================

    def save_file(self):

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )

        if not filename:
            return

        try:
            save_data(
                self.students,
                self.instructors,
                self.courses,
                filename
            )

            messagebox.showinfo(
                "Success",
                "Data saved successfully."
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error)
            )


    # =========================================================
    # LOAD
    # =========================================================

    def load_file(self):

        filename = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")]
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

            messagebox.showinfo(
                "Success",
                "Data loaded successfully."
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error)
            )


# =============================================================
# RUN APPLICATION
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SchoolManagementApp(root)

    root.mainloop()