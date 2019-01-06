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
    return None


def insert_student(student_type, sum_of_all):
    return None


def insert_course(course_id, course_name, student_type, course_capacity, classroom, iterations):
    return None

def insert_object(object):
    first_letter = object[0]
    object = object.remove(first_letter)
    if first_letter == 'C':
        insert_course(*object)
    if first_letter == "S":
        insert_student(*object)
    if first_letter == "R":
        insert_classroom(*object)


if not os.path.isfile("classes.db"):
    conn = sqlite3.connect("classes.db")
    create_tables()

with open(sys.argv[1], "rb") as file:
    line = file.readline()
    insert_object(line.split(','))
