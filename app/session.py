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
    def __init__(self):
        self.current_user_id = None  # Start with no user logged in
        
    def login(self, user_id):
        self.current_user_id = user_id
        
    def logout(self):
        self.current_user_id = None
        
    @property
    def is_authenticated(self):
        return self.current_user_id is not None

# Initialize session with no user logged in
SESSION = Session()


