# Filename: university.py
# Description: This module contains university related objects
# Inputs: N/A
# Output: N/A
# Authors: Xavier Ruyle, Andrew Ward
# Creation Date: 10/24/2024

from db import query


class University:
    """
    Class which contains information about a university
    Identified mainly by the acronym of the university (e.g KU).
    """
    def __init__(self, id, name, acronym, description, logo = None):
        self.id          = id          # db id
        self.name        = name        # ex: University of Kansas
        self.acronym     = acronym     # ex: KU
        self.description = description # ex: Home of of the JayHawks
        self.logo        = logo        # Filepath to the logo

    @property
    def courses(self):
        """
        Courses getter. Returns a list of all the courses
        that belong to the calling university in the DB.
        """

        # Yeah, this is a bit jank.
        from course import Course

        # Convert each database row into a Course object.
        return [Course(*params, self.id) for params in query(
            """
                SELECT id, name, description, course_number, department FROM courses
                WHERE university = ?;
            """,
            (self.id,)
        )]

    @staticmethod
    def get_university_by_id(id: int):
        """
        Get a university by its database id.
        Return None if university not found.
        """

        params = query(
            "SELECT id, name, acronym, description FROM universities WHERE id = ?;",
            (id,),
            count = 1
        )
        if not params: return None # University not found
        return University(*params) # Construct university object

    @staticmethod
    def get_university_by_name(name: str):
        """
        Get a university by its vernacular name (e.g. Software Engineering II).

        :param name: Common name of the uni (ex: Software Engineering II).
        :returns: University object or None if course not found.
        """

        params = query(
            "SELECT id, name, acronym, description FROM universities WHERE name = ?;",
            (name,),
            count = 1
        )
        if not params: return None # University not found
        return University(*params) # Construct university object

    @staticmethod
    def get_university_by_acronym(acronym: str):
        """
        Get a university by its acronym (e.g. KU, KSTATE, etc.).

        :param name: Acronym of the university (ex: KU).
        :returns: University object or None if course not found.
        """

        params = query(
            "SELECT id, name, acronym, description FROM universities WHERE acronym = ?;",
            (acronym.upper(),),
            count = 1
        )
        if not params: return None # University not found
        return University(*params) # Construct university object

    @staticmethod
    def get_all_universities():
        """
        Return all universities from the database.
        """

        # @TODO: Memoize this. This has bad performance rn.

        # Convert database rows into University objects
        return [University(*params) for params in query(
            "SELECT id, name, acronym, description FROM universities;"
        )]
