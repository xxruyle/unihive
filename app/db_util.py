# Filename: db_util.py
# Description: This module is utility for storing of object data in DB and locally 
# Inputs: Other modules/classes, university, course, session, user, flask
# Output: Storing methods and checking if objects exist etc 
# Authors: Xavier Ruyle
# Creation Date: 10/25/2024

from university import *
from course import * 
from session import * 
from user import * 
from db import query

################################################################################

def store_course(course_name, course_number, department, university): 
    return query(
        """
            INSERT INTO courses (name, description, course_number, department, hours, university)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
        (course_name, "", course_number, department.id, 0, university.id)
    )

def store_university_follow(university): 
    user = USERS[SESSION.current_user_id]
    return query(
        "INSERT INTO user_universities (user, university) VALUES (?, ?);",
        (user.id, university.id)
    )

def store_course_follow(course): 
    user = USERS[SESSION.current_user_id]
    return query(
        "INSERT INTO user_courses (user, course) VALUES (?, ?);",
        (user.id, course.id)
    )

def store_course_info(course, difficulty, grade, hours): 
    user = USERS[SESSION.current_user_id]
    return course.store_info(user, difficulty, grade, hours)

def store_professor_info(course, professor_full_name): 
    user = USERS[SESSION.current_user_id]
    return course.store_info(user, instructor = professor_full_name)

def get_uni_and_course_from_route(university_acronym, course_name_combined):
    university = University.get_university_by_acronym(university_acronym)
    
    if university is None: 
        return (None, None)

    return (
        university,
        Course.get_course_by_name_combined(university, course_name_combined)
    )

################################################################################

def store_department(department_name, abbreviation, university):
    return query(
        """
            INSERT INTO departments (name, abbreviation, university)
            VALUES (?, ?, ?);
        """,
        (department_name, abbreviation.upper(), university.id)
    )

################################################################################

def store_university(university_name, university_acronym, description = None): 
    return query(
        """
            INSERT INTO universities (name, acronym, description)
            VALUES (?, ?, ?);
        """,
        (university_name, university_acronym.upper(), description)
    )
    
################################################################################