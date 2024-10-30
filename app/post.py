import datetime 

class Post: 
    def __init__(self, user, title, body): 
        self.user = "test-user" 
        self.title  = title 
        self.body  = body 
        self.date_posted = datetime.date.today()
        self.replies = [] 


class Reply(Post): 
    def __init__(self):
        super().__init__()



