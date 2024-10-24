# Filename: university.py
# Description: This module contains university related objects 
# Inputs: N/A
# Output: UNIVERSITIES dict container 
# Authors: Xavier Ruyle
# Creation Date: 10/24/2024

UNIVERSITIES = {} # placeholder for database 
class University: 
    '''
    Class which contains information about a university 
    Identified mainly by the acronym of the university (e.g KU)
    '''
    def __init__(self, id, full_name, name): 
        self.id = id  # db id 
        self.full_name = full_name # ex: University of Kansas 
        self.acronym = name  # ex: KU
        self.courses = {} # eecs-581 key, course object is the value 
