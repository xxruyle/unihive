# Filename: user.py
# Description: This module contains user related objects and methods
# Inputs: N/A
# Output: USERS container
# Authors: Xavier Ruyle, Andrew Ward
# Creation Date: 10/24/2024

from db import query
from university import University
from course import Course
from session import SESSION

class User:
    """
    Class which contains information about users on the site
    """
    def __init__(self, id, name):
        self.id          = id   # db id
        self.name        = name # full name of the user
        self.profile_img = None # image id (stored on db?)

    @property
    def followed_universities(self):
        """
        Getter for the universities that the user follows.
        Returns a list of the followed universities.
        """

        # Convert each database row to a University object.
        return [University(*params) for params in query(
            """
                SELECT DISTINCT universities.id, name, acronym, description
                FROM universities INNER JOIN user_universities
                ON universities.id = user_universities.university
                WHERE user = ?;
            """,
            (self.id,)
        )]

    @property
    def followed_courses(self):
        """
        Getter for the courses that the user follows.
        Returns a list of the followed courses.
        """

        # Convert each database row to a Course object.
        return [Course(*params) for params in query(
            """
                SELECT DISTINCT courses.id, name, description, course_number, department, university
                FROM courses INNER JOIN user_courses
                ON courses.id = user_courses.course
                WHERE user = ?;
            """,
            (self.id,)
        )]

    def _get_image_db(self):
        """
        Retrieves an image file from the db
        """
        pass

USERS = {SESSION.current_user_id: User(1, "DEV")}  # USERS container (user id as key, User object instance as value)