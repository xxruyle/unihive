posts = []

class Post: 
    def __init__(self,university_id, course_id, user): 
        self.course_id = course_id # what course 
        self.user = user  
        self.replies = [] 


class Reply(Post): 
    def __init__(self):
        super().__init__()



