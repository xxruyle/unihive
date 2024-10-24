class Course: 
    def __init__(self, id, course_id, department, name): 
        self.id = id # db id  
        self.course_id = course_id # ex: 581
        self.department = department  # ex: EECS
        self.name = name  # ex: Software Engineering
        self.professors = set() 
        self.difficulty = 1
        self.average_grade = "Unknown"
        self.credit_hours = 0
        self.grade_submission_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        self.num_info_submissions = 0 # how many people submitted course info 

    '''
    takes in difficulty, grade, and credit hours and stores them in the course member variables
    '''
    def store_info(self, grade, difficulty, credit_hours): 
        self.num_info_submissions += 1 
        self.difficulty = self._averagize_difficulty(difficulty) 
        self._averagize_grade(grade) 
        self.credit_hours = credit_hours 


    '''gets the new average difficulty for store_info '''
    def _averagize_difficulty(self, difficulty): 
        return (self.difficulty*(self.num_info_submissions-1) + difficulty) / self.num_info_submissions

    '''gets the new average grade for store info'''
    def _averagize_grade(self, grade):
        self.grade_submission_count[grade] += 1 
        self.average_grade = max(self.grade_submission_count, key=lambda x: self.grade_submission_count[x])


