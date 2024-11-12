# Filename: db_util.py
# Description: This module is utility for storing of object data in DB and locally
# Inputs: Other modules/classes, university, course, session, user, flask
# Output: Storing methods and checking if objects exist etc
# Authors: Xavier Ruyle, Andrew Ward
# Creation Date: 10/25/2024

from course import *
from db import query
from department import *
from post import *
from session import *
from university import *
from user import *

################################################################################

def store_course(course_name: str, course_number: int, department: Department):
    """
    Create a new course entry in the database. Complete
    with a name, number, department, and university.

    :param course_name: The course name (ex: Software Eng II).
    :param course_number: The number of the course (ex: 581).
    :param department: The department the course belongs to.
    """

    return query(
        """
            INSERT INTO courses (name, description, course_number, department, hours, university)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
        (course_name, "", course_number, department.id, 0, department.university.id)
    )

def store_university_follow(university: University):
    """
    Make the current user follow a university.
    :param university: The university the user will follow.
    """

    user = USERS[SESSION.current_user_id] # @TODO: Replace this
    return query(
        "INSERT INTO user_universities (user, university) VALUES (?, ?);",
        (user.id, university.id)
    )

def store_course_follow(course: Course):
    """
    Make the current user follow a course.
    :param course: The course the user will follow.
    """

    user = USERS[SESSION.current_user_id] # @TODO: Replace this
    return query(
        "INSERT INTO user_courses (user, course) VALUES (?, ?);",
        (user.id, course.id)
    )

def store_course_info(course: Course, difficulty: float, grade: Grade, hours: int):
    """
    Store course information submitted by the current
    user. Includes difficulty, grade, and hours.

    :param course: The course that the info belongs to.
    :param difficulty: The difficulty rating (1-10).
    :param grade: The grade the user received (F-A).
    :param hours: The credit hours of the course.
    """

    user = USERS[SESSION.current_user_id] # @TODO: Replace this
    return course.store_info(user, difficulty, grade, hours)

def store_professor_info(course: Course, professor_full_name: str):
    """
    Store course instructor name information
    submitted by the user for a given course.

    :param course: The course that the instructor taught.
    :param professor_full_name: The instructor's full name.
    """

    user = USERS[SESSION.current_user_id] # @TODO: Replace this
    return course.store_info(user, instructor = professor_full_name)

def get_uni_and_course_from_route(university_acronym: str, course_name_combined: str):
    """
    Helper function that returns university and course tuple
    for a given university acronym and course combined name.
    For example: valid parameters would be "KU", "EECS-581".

    :param university_acronym: The university acronym (ex: KU).
    :param course_name_combined: The course full name (ex: EECS-581).
    """

    # Get the university based on the acronym provided.
    university = University.get_university_by_acronym(university_acronym)

    # If the university doesn't exist,
    # short circuit into double None.
    if university is None:
        return (None, None)

    # Return the university and course as a tuple
    # can be destructured by the caller for ease.
    return (
        university,
        Course.get_course_by_name_combined(university, course_name_combined)
    )

################################################################################

def store_syllabus(course_name_combined: str, file_name: str, file: bytes): 
    """
    Upload syllabus to the database using, the course_name_combined, file_name,
    and file (in bytes) 

    :param coursename: Course name combined (ex: EECS-388)
    :param file_name: File name (ex: eecs388-syllabus)
    :param file: Actual file data in bytes 
    """
    # TODO: store syllabus course 
    return query(
        """
        INSERT INTO syllabus (coursename, filename, file)
        VALUES (?, ?, ?);
        """,
        (course_name_combined, file_name, file)
    )

def store_department(department_name: str, abbreviation: str, university: University):
    """
    Create a new department in the database using
    the provided name, abbreviation, and university.

    :param department_name: Name (ex: Electrical Engineering & Comp Sci).
    :param abbreviation: The abbreviation for new department (ex: EECS).
    :param university: The university that the new department belongs to.
    """

    return query(
        """
            INSERT INTO departments (name, abbreviation, university)
            VALUES (?, ?, ?);
        """,
        (department_name, abbreviation.upper(), university.id)
    )

################################################################################

def store_university(university_name: str, university_acronym: str, description: str = None):
    """
    Create a new university in the database using
    the provided name, acronym and description.

    :param university_name: Name of university (ex: University of Kansas)
    :param university_acronym: University Acronym (ex: KU, KSTATE, ect.)
    :param description: Optional description (ex: Best school in KS...)
    """

    return query(
        """
            INSERT INTO universities (name, acronym, description)
            VALUES (?, ?, ?);
        """,
        (university_name, university_acronym.upper(), description)
    )

################################################################################

def store_post(course: Course, title: str, post_body: str):
    """
    Create a new post in the database for a given
    course complete with title and post contents.

    :param course: The course that the post belongs to.
    :param title: The title (identifier) of the new post.
    :param post_body: The contents of the new post.
    """

    user = USERS[SESSION.current_user_id] # @TODO: Replace this

    # Insert a new post into the database.
    return query(
        """
        INSERT INTO posts (title, content, author, course)
        VALUES (?, ?, ?, ?);
        """,
        (title, post_body, user.username, course.id)
    )

################################################################################

def sort_courses(sort_type : str, university: University): 
    """
     Change University object's sort_course_type
     This affects the university @property courses method 

    :param sort_type: The available sort type options defined in universty_home.html.
    :param university: The university object.
    """
    if sort_type == "Date Created":
        university.sort_course_type = "created" 
    elif sort_type == "Department": 
        university.sort_course_type = "department" 

def sort_posts(sort_type : str, course: Course): 
    """
     Change University object's sort_course_type
     This affects the university @property courses method 

    :param sort_type: The available sort type options defined in universty_home.html.
    :param university: The university object.
    """
    if sort_type == "Date Created": 
        course.sort_post_type = "Date Created" 
    elif sort_type == "Popularity": 
        course.sort_post_type = "Popularity" 

