# Filename: department.py
# Description: This module contains department related objects
# Inputs: N/A
# Output: N/A
# Authors: Andrew Ward
# Creation Date: 10/24/2024

from db import query
from university import University

class Department:
    def __init__(self, id, name, abbreviation, university_id):
        self.id           = id                                             # Database ID
        self.name         = name                                           # Name of department (ex: Electrical Engineering)
        self.abbreviation = abbreviation                                   # Department abbreviation (ex: EECS)
        self.university   = University.get_university_by_id(university_id) # University department belongs to

    @staticmethod
    def get_department_by_id(id: int):
        """
        Get a department by its database id.
        Return None if department not found.
        """

        params = query(
            "SELECT id, name, abbreviation, university FROM departments WHERE id = ?",
            (id,),
            count = 1
        )
        if not params: return None # Department not found
        return Department(*params) # Construct department object

    @staticmethod
    def get_department_by_abbreviation(university: University, abbreviation: str):
        """
        Get a department in a university by its
        abbreviation (ex: EECS) from the database.

        :param university: The university the department belongs to.
        :param abbreviation: The department abbreviation (ex: EECS).
        :return: Department object or None if not found.
        """

        params = query(
            """
                SELECT id, name, abbreviation, university FROM departments
                WHERE university = ? AND abbreviation = ?;
            """,
            (university.id, abbreviation.upper()),
            count = 1
        )
        if not params: return None # Department not found
        return Department(*params) # Construct department object