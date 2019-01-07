import os
import sqlite3
from create_db import *

DB_NAME = "schedule.db"


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


def coursesIsEmpty(cursor):
    cursor.execute("SELECT * FROM courses")
    line = cursor.fetchone()
    if line is None:
        return True
    return False


def increase_students_occupied_by_deleted_course(count, grade):
    sql = """
    UPDATE students 
    SET  count = count + ? WHERE grade = ?
    """
    val = (count, grade)
    cursor.execute(sql, val)
    conn.commit()


def update_classroom_decrease_time(cr_id):
    sql = """
    UPDATE classrooms 
    SET  current_course_time_left = current_course_time_left - 1
    WHERE id = ?
    """
    val = (cr_id,)
    cursor.execute(sql, val)
    conn.commit()


def update_course_after_assignment(c_id, cr_id):
    sql = """
    UPDATE courses 
    SET  class_id = ? WHERE id = ?
    """
    val = (cr_id, c_id)
    cursor.execute(sql, val)
    conn.commit()


def update_student_by_course(count, grade):
    sql = """
    UPDATE students 
    SET  count = count - ? WHERE grade = ?
    """
    val = (count, grade)
    cursor.execute(sql, val)
    conn.commit()


def delete_course_by_id(c_id):
    sql = """
    DELETE from courses 
    WHERE id = ?
    """
    val = (c_id,)
    cursor.execute(sql, val)
    conn.commit()


def format_this_tuple(tuple_object):
    return tuple_object[1] + ": " + tuple_object[0]


def get_classroom_and_course_data(cr_id):
    cursor.execute(
        "SELECT courses.course_name, classrooms.location FROM classrooms INNER JOIN courses ON courses.class_id = classrooms.id WHERE classrooms.id = ?",
        (
            cr_id,))
    return cursor.fetchone()


def update_classroom_by_course(c_id, c_length, cr_id):
    sql = """
    UPDATE classrooms 
    SET current_course_id = ? , current_course_time_left = ? WHERE id = ?
    """
    val = (c_id, c_length, cr_id)
    cursor.execute(sql, val)
    conn.commit()


if os.path.isfile(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    iteration_id = 0
    while not coursesIsEmpty(cursor):
        cursor.execute("SELECT * FROM classrooms")
        classrooms = cursor.fetchall()
        for classroom in classrooms:
            if classroom[3] == 0:  # Check if the room is ready for new course
                if classroom[2] != 0:  # check if there is a course_id
                    # update students with the course amount (that has finished, and delete the course).
                    cursor.execute("SELECT student, number_of_students FROM courses WHERE id = ?", (classroom[2],))
                    students = cursor.fetchone()
                    increase_students_occupied_by_deleted_course(students[1], students[0])
                    print("(" + str(iteration_id) + ")" + format_this_tuple(get_classroom_and_course_data(classroom[0])) + " is done")
                    delete_course_by_id(classroom[2])
                # Assignment: Fetch one course
                cursor.execute("SELECT * FROM courses WHERE class_id = ? ", (classroom[0],))
                course = cursor.fetchone()
                if course is not None:
                    course_id = course[0]
                    students_of_course = course[2]
                    number_of_students = course[3]
                    course_length = course[5]
                    # update classroom
                    update_classroom_by_course(course_id, course_length, classroom[0])
                    # update students
                    update_student_by_course(number_of_students, students_of_course)
                    # update course
                    update_course_after_assignment(course_id, classroom[0])
                    print("(" + str(iteration_id) + ")" + format_this_tuple(get_classroom_and_course_data(classroom[0])) + " is schedule to start")
            else:
                update_classroom_decrease_time(classroom[0])
                data = get_classroom_and_course_data(classroom[0])
                print ("(" + str(iteration_id) + ") " + data[1] + ": occupied by "+data[0])
        iteration_id += 1
        print_all_tables()
os.remove(DB_NAME)
