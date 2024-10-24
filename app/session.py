# Filename: session.py
# Description: This module contains session related objects and methods
# Inputs: N/A
# Output: DEBUG SESSION object instance 
# Authors: Xavier Ruyle
# Creation Date: 10/24/2024

class Session: 
    '''
    Class which identifies current user from the database
    Informs the website what user is viewing the pages
    '''
    def __init__(self, current_user_id):
        self.current_user_id = current_user_id

SESSION = Session(1) 



