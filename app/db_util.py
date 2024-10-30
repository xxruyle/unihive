# Filename: db_util.py
# Description: This module is utility for storing of object data in DB and locally 
# Inputs: Other modules/classes, university, course, session, user, flask
# Output: Storing methods and checking if objects exist etc 
# Authors: Xavier Ruyle
# Creation Date: 10/25/2024

from university import *
from course import * 
from session import * 
from post import * 
from user import * 

def store_university_follow(university_acro): 
    USERS[SESSION.current_user_id].followed_universities.add(UNIVERSITIES[university_acro]) # STORE: User followed university 

def store_course_follow(university_acro, course): 
    USERS[SESSION.current_user_id].followed_courses.add(UNIVERSITIES[university_acro].courses[course]) # STORE: User followed course 

def store_course_info(course, grade, difficulty, credit_hours): 
    course.store_info(grade, difficulty, credit_hours)

def store_professor_info(course, professor_full_name): 
    course.professors.add(professor_full_name)


def store_university(university_acro, university_name): 
    university = University(len(UNIVERSITIES) + 1, university_name, university_acro)
    UNIVERSITIES[university_acro] = university # STORE: University 

def store_post(course_obj, title, post_body): 
    post_obj = Post(course_obj, title, post_body)
    course_obj.posts.append(post_obj)



def university_exists(university_acro): 
    return university_acro in UNIVERSITIES

def course_exists(university_acro, department_course_number): 
    return department_course_number in UNIVERSITIES[university_acro].courses

def store_course(id, course_number, department, course_name, university_acro) : 
    department_course_number = f"{department}-{course_number}"
    course_obj = Course(id, course_number, department, course_name, university_acro)
    UNIVERSITIES[university_acro].courses[department_course_number] = course_obj # STORE: Course
    

