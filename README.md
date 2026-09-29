# EECE 435L Labs

This repository contains laboratory work and exercises for **EECE 435L**.

The main project in this repository is a **School Management System** developed incrementally using Python. The different parts demonstrate object-oriented programming, graphical user interfaces, data persistence, and database management.

## Project Overview

The School Management System manages:

- Students
- Instructors
- Courses
- Student course registration
- Instructor course assignments
- Record searching and management
- Persistent data storage

The project is divided into multiple parts, with each part adding new functionality.

## Project Structure

```text
EECE-435L-Labs/
│
├── part1.py
├── part2.py
├── part3.py
├── part4.py
│
├── data.json
├── school.db
├── school_backup.db
│
├── docs/
├── output/
├── screenshots/
│
├── Lab 3-Documentation.docx
└── Lab 4-Git.docx
```

## Parts

### Part 1 — Object-Oriented Programming & JSON

`part1.py` implements the core data model of the School Management System.

It includes classes such as:

- `Person`
- `Student`
- `Instructor`
- `Course`

The system supports student registration, instructor assignment, input validation, and saving/loading application data using **JSON**.

### Part 2 — Tkinter GUI

`part2.py` introduces a graphical user interface using **Tkinter**.

The GUI provides separate sections for:

- Students
- Instructors
- Courses
- Registration / Assignment
- Records

Users can manage the school system through a desktop interface instead of interacting directly with the Python classes.

### Part 3 — PyQt5 GUI

`part3.py` rebuilds and expands the graphical interface using **PyQt5**.

Features include:

- Adding students, instructors, and courses
- Registering students in courses
- Assigning instructors to courses
- Viewing records in tables
- Searching records
- Editing and deleting records
- Saving and loading data
- Exporting records to CSV

### Part 4 — SQLite Database

`part4.py` extends the application by replacing file-based storage with an **SQLite relational database**.

The database stores:

- Students
- Instructors
- Courses
- Enrollments
- Course assignments

Additional database functionality includes:

- Persistent storage
- SQL queries
- Foreign-key relationships
- Record searching
- Database backup
- Database restoration

## Technologies Used

- Python
- Object-Oriented Programming
- JSON
- Tkinter
- PyQt5
- SQLite
- SQL
- CSV
- Git
- GitHub

## Requirements

Python 3 is required.

For the PyQt5 versions of the application, install PyQt5 using:

```bash
pip install PyQt5
```

SQLite and Tkinter are included with most standard Python installations.

## Running the Project

Clone the repository:

```bash
git clone https://github.com/KevinAntoun/EECE-435L-Labs.git
```

Navigate into the repository:

```bash
cd EECE-435L-Labs
```

Run one of the project parts:

```bash
python part1.py
```

```bash
python part2.py
```

```bash
python part3.py
```

```bash
python part4.py
```

For the latest database-backed version, use:

```bash
python part4.py
```

## Database

The SQLite version uses:

```text
school.db
```

A backup database may also be stored as:

```text
school_backup.db
```

The application provides functionality for backing up and restoring the database.

## Documentation

Additional lab documentation can be found in:

- `Lab 3-Documentation.docx`
- `Lab 4-Git.docx`
- `docs/`
- `screenshots/`
- `output/`

## Author

**Kevin Antoun**

## Disclaimer

This repository contains coursework and laboratory material created for educational purposes.