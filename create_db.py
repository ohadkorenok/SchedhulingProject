import os
import sqlite3
import atexit
import sys

DB_NAME = "schedule.db"

def create_tables(conn):
    conn.executescript("""
    
    CREATE TABLE courses(
    id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    student TEXT NOT NULL,
    number_of_students INTEGER NOT NULL,
    class_id INTEGER REFERENCES classrooms(id),
    course_length INTEGER NOT NULL
    );
    
    CREATE TABLE students(
    grade TEXT PRIMARY KEY,
    count INTEGER NOT NULL
    );
    
    CREATE TABLE classrooms(
    id INTEGER PRIMARY KEY,
    location TEXT NOT NULL,
    current_course_id INTEGER NOT NULL,
    current_course_time_left INTEGER NOT NULL
    );
    """)


def print_courses():
    print("courses")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    for i in cursor.fetchall():
        print(i)


def print_classrooms():
    print("classrooms")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classrooms")
    for i in cursor.fetchall():
        print(i)


def print_students():
    print("students")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    for i in cursor.fetchall():
        print(i)


def print_all_tables():
    print_courses()
    print_classrooms()
    print_students()


def insert_classroom(conn, room_id, location):
    conn.execute("""
    INSERT INTO classrooms (id, location, current_course_id, current_course_time_left) VALUES(?,?, ?, ?)
    """, [int(room_id), location, 0, 0])
    conn.commit()


def insert_student(conn, student_type, sum_of_all):
    conn.execute("""
    INSERT INTO students (grade, count) VALUES(?,?)
    """, [student_type, int(sum_of_all)])
    conn.commit()


def insert_course(conn, course_id, course_name, student_type, course_capacity, class_id, iterations):
    conn.execute("""
    INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length) VALUES(?,?,?,?,?,?)
    """, [int(course_id), course_name, student_type, int(course_capacity), int(class_id), int(iterations)])
    conn.commit()


def insert_object(conn, row_object):
    first_letter = row_object[0]
    row_object.remove(first_letter)
    if first_letter == 'C':
        insert_course(conn, *row_object)
    if first_letter == "S":
        insert_student(conn, *row_object)
    if first_letter == "R":
        insert_classroom(conn, *row_object)


if not os.path.isfile(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    create_tables(conn)
    with open(sys.argv[1], "r") as file:
        line = file.readline()
        while line != '':
            line = line[:-1]
            lineList = line.split(',')
            insert_object(conn, lineList)
            line = file.readline()
    print_all_tables()

