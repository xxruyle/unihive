# Filename: post.py
# Description: This module contains post related objects and methods
# Inputs: N/A
# Output: N/A
# Authors: Xavier Ruyle, Andrew Ward
# Creation Date: 10/24/2024

import datetime

from course import Course
from db import query
from user import User


class Post: 
    def __init__(self, id, created, title, content, author, course_id): 
        self.id      = id                                 # Database ID       
        self.created = created                            # Date Created  
        self.title   = title                              # Title of post        
        self.content = content                            # Post body  
        self.author  = author                        # @TEMPORARY, author   
        self.course  = Course.get_course_by_id(course_id) # Course post belongs to  

    @property
    def replies(self):
        """
        Post replies getter. Returns a list of all
        the replies that belong to a post. This is
        not recursive (sub-replies not shown).
        """

        return [Post(*params, self.id) for params in query(
            """
                SELECT id, created, title, content, author, course FROM posts
                WHERE parent = ?;
            """,
            (self.id,)
        )]



class Reply(Post): 
    def __init__(self):
        super().__init__()



