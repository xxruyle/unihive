# Filename: user.py
# Description: This module contains user related objects and methods
# Inputs: N/A
# Output: USERS container 
# Authors: Xavier Ruyle
# Creation Date: 10/24/2024

USERS = {}  # USERS container (user id as key, User object instance as value)
class User: 
    '''
    Class which contains information about users on the site 
    '''
    def __init__(self, id, name): 
        self.id = id # db id
        self.name = name # full name of the user
        self.profile_img = None # image id (stored on db?)  
        self.followed_universities = set() # contains university object
        self.followed_courses = set() # contains course object 


    def _get_image_db(self): 
        '''
        Retrieves an image file from the db
        '''
        pass 
