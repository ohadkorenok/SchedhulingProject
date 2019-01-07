import os
import sqlite3
import atexit
import sys


def create_tables():
    return conn.executescript("""
    
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


def insert_classroom(room_id, location):
    cursor.execute("INSERT INTO classrooms VALUES(?,?, ?, ? )", (int(room_id), location, 0, 0))


def insert_student(student_type, sum_of_all):
    cursor.execute("INSERT INTO students VALUES(?,?)", (student_type, int(sum_of_all)))


def insert_course(course_id, course_name, student_type, course_capacity, class_id, iterations):
    cursor.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)",
                   (int(course_id), course_name, student_type, course_capacity, class_id, iterations))


def insert_object(row_object):
    first_letter = row_object[0]
    row_object = row_object.remove(first_letter)
    if first_letter == 'C':
        insert_course(*row_object)
    if first_letter == "S":
        insert_student(*row_object)
    if first_letter == "R":
        insert_classroom(*row_object)


if not os.path.isfile("classes.db"):
    conn = sqlite3.connect("classes.db")
    cursor = conn.cursor()
    create_tables()

with open(sys.argv[1], "rb") as file:
    line = file.readline()
    insert_object(*line.split(','))
