# Filename: university.py
# Description: This module contains university related objects 
# Inputs: N/A
# Output: UNIVERSITIES dict container 
# Authors: Xavier Ruyle, Andrew Ward
# Creation Date: 10/24/2024

from db import query

class University: 
    '''
    Class which contains information about a university 
    Identified mainly by the acronym of the university (e.g KU)
    '''
    def __init__(self, id, name, acronym, description, logo = None): 
        self.id          = id          # db id 
        self.name        = name        # ex: University of Kansas 
        self.acronym     = acronym     # ex: KU
        self.description = description # ex: Home of of the JayHawks
        self.logo        = logo
    
    @staticmethod
    def get_university_by_id(id):
        params = query(
            "SELECT id, name, acronym, description FROM universities WHERE id = ?;", 
            (id,),
            count = 1
        )
        if not params: return None
        return University(*params)
    
    @staticmethod
    def get_university_by_name(name):
        params = query(
            "SELECT id, name, acronym, description FROM universities WHERE name = ?;",
            (name,),
            count = 1
        )
        if not params: return None
        return University(*params)

    @staticmethod
    def get_university_by_acronym(acronym):
        params = query(
            "SELECT id, name, acronym, description FROM universities WHERE acronym = ?;",
            (acronym.upper(),),
            count = 1
        )
        if not params: return None
        return University(*params)

    @staticmethod
    def get_all_universities():
        
        # @TODO: Memoize this. This has ridiculously bad performance rn.

        return [University(*params) for params in query(
            "SELECT id, name, acronym, description FROM universities;"
        )]

    @property
    def courses(self):

        # Yeah, this is a bit jank.
        from course import Course

        return [Course(*params, self.id) for params in query(
            """
                SELECT id, name, description, course_number, department FROM courses
                WHERE university = ?;
            """,
            (self.id,)
        )]