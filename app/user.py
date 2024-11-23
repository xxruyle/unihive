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
from datetime import datetime

class User:
    """
    Class which contains information about users on the site
    """
    def __init__(self, id, username):
        self.id          = id       # db id
        self.username    = username # full name of the user
        self.profile_img = None     # image id (stored on db?)
        self.created     = datetime.now()

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

    @staticmethod
    def get_user_by_id(id: int):
        """
        Get a user by its database id.
        Return None if user not found.
        """

        params = query(
            """
                SELECT id, username FROM users
                WHERE id = ?;
            """,
            (id,),
            count = 1
        )
        if not params: return None # User not found
        return User(*params)       # Construct User object

    @staticmethod
    def get_user_by_username(username: str):
        """
        Get a User by their username.
        :param username: The username.
        """

        # @TEMPORARY: This is just a stopgap to
        # allow the session based code to work
        # for development purposes only.
        for user in list(USERS.values()):
            if user.username == username:
                return user

        # Query the database for user data.
        params = query(
            f"""
                SELECT id, username FROM users
                WHERE username = ?;
            """,
            (username,),
            count = 1
        )
        if not params: return None # Course not found
        return User(*params)       # Construct course object

    def _get_image_db(self):
        """
        Retrieves an image file from the db
        """
        pass

USERS = {SESSION.current_user_id: User(1, "DEV")}  # USERS container (user id as key, User object instance as value)