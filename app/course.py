# Filename: course.py
# Description: This module contains course related objects and methods
# Inputs: N/A
# Output: N/A
# Authors: Xavier Ruyle
# Creation Date: 10/24/2024

class Course: 
    def __init__(self, id, course_id, department, name, university_acro): 
        self.id = id # db id  
        self.course_id = course_id # ex: 581
        self.department = department  # ex: EECS
        self.name = name  # ex: Software Engineering
        self.university_acro = university_acro
        self.name_combined = self.department + "-" + str(self.course_id)  # ex: EECS-581
        self.professors = set()  # set of strings 
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


