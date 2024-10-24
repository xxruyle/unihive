UNIVERSITIES = {} # placeholder for database 
class University: 
    def __init__(self, id, full_name, name): 
        self.id = id  # db id 
        self.full_name = full_name # ex: University of Kansas 
        self.name = name  # ex: KU
        self.courses = {} # eecs-581 key, course object is the value 
