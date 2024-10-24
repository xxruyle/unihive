users = []  # placeholder for users 
class User: 
    def __init__(self, id, name): 
        self.id = id # db id
        self.name = name
        self.profile_img = None
        self.followed_universities = set() # contains university acronyms
        self.followed_courses = set() # contains course department-coursenum (Ex: "EECS-581") 
