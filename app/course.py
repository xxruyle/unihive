# Filename: course.py
# Description: This module contains course related objects and methods
# Inputs: N/A
# Output: N/A
# Authors: Xavier Ruyle, Andrew Ward
# Creation Date: 10/24/2024

from enum import IntEnum
from db import query
from university import University
from department import Department

COURSE_PARAMS = "courses.id, courses.name, description, course_number, department, courses.university"

class Course: 
    def __init__(self, id, name, description, course_number, department_id, university_id): 
        self.id             = id            # db id  
        self.name           = name          # ex: Software Engineering
        self.description    = description   # ex: An introduction to software
        self.course_number  = course_number # ex: 581
        self.department     = Department.get_department_by_id(department_id)
        self.university     = University.get_university_by_id(university_id)

        self.name_combined = self.department.name + "-" + str(self.course_number) # ex: EECS-581

    @staticmethod
    def get_course_by_id(id):
        params = query(
            f"SELECT {COURSE_PARAMS} FROM courses WHERE id = ?",
            (id,), 
            count = 1
        )
        if not params: return None
        return Course(*params)

    @staticmethod 
    def get_course_by_name_combined(university, name_combined):
        params = query(
            f"""
                SELECT {COURSE_PARAMS} FROM courses 
                INNER JOIN departments 
                ON courses.department = departments.id
                WHERE courses.university = ?
                AND (departments.abbreviation || '-' || courses.course_number) = ?;
            """, 
            (university.id, name_combined.upper()), 
            count = 1
        )
        if not params: return None
        return Course(*params)

    @staticmethod
    def get_course_by_name(university, name):
        params = query(
            f"SELECT {COURSE_PARAMS} FROM courses WHERE name = ? AND university = ?",
            (name, university.id), 
            count = 1
        )
        if not params: return None
        return Course(*params)

    @staticmethod
    def get_course_by_course_number(university, course_number):
        params = query(
            f"SELECT {COURSE_PARAMS} FROM courses WHERE course_number = ? AND university = ?",
            (course_number, university.id), 
            count = 1
        )
        if not params: return None
        return Course(*params)

    def store_info(self, user, difficulty = None, grade = None, credit_hours = None, instructor = None):
        """
        Takes in difficulty, grade, and credit hours and stores them in the DB.
        """

        user_already_submitted = bool(query(
            """
                SELECT * FROM course_ratings
                WHERE user = ? AND course = ?;
            """, 
            (user.id, self.id),
            count = 1
        ))

        if user_already_submitted:
            query(
                """
                    UPDATE course_ratings SET 
                        difficulty = COALESCE(?, difficulty), 
                        grade      = COALESCE(?, grade),
                        hours      = COALESCE(?, hours),
                        instructor = COALESCE(?, instructor)
                    WHERE user = ? AND course = ?;
                """,
                (difficulty, grade, credit_hours, instructor, user.id, self.id)
            )
        else:
            query(
                """
                    INSERT INTO course_ratings (user, course, difficulty, grade, hours, instructor)
                    VALUES (?, ?, ?, ?, ?, ?);
                """,
                (user.id, self.id, difficulty, grade, credit_hours, instructor)
            )

    @property
    def average_difficulty(self):
        """Average difficulty getter."""

        difficulties = query(
            """
                SELECT difficulty FROM course_ratings
                WHERE course = ? AND difficulty IS NOT NULL;
            """,
            (self.id,)
        )

        if not len(difficulties):
            return None

        # I kind of regressed the performance here. If we
        # run into performance issues I will reimplement 
        # the exponential moving average algorithm. - AW
        
        return sum(i[0] for i in difficulties) / len(difficulties)

    
    @property
    def average_grade(self):
        """Average grade getter."""

        grades = query(
            """
                SELECT grade FROM course_ratings
                WHERE course = ? AND grade IS NOT NULL;
            """,
            (self.id,)
        )

        if not len(grades):
            return None

        mean = sum(i[0] for i in grades) / len(grades)
        return Grade(round(mean))

    @property
    def credit_hours(self):
        """Mode credit hours getter."""

        hours = query(
            """
                SELECT hours FROM course_ratings
                WHERE course = ? AND hours IS NOT NULL;
            """,
            (self.id,)
        )

        if not len(hours):
            return None
        
        # Get the mode credit_hours. Average would
        # be a bit strange here.

        hour_table = {}
        for submission in hours:
            if submission[0] in hour_table:
                hour_table[submission[0]] += 1
            else:
                hour_table[submission[0]] = 1

        return max(hour_table, key = lambda x: hour_table[x])

    @property
    def instructors(self):
        """Instructors that supposedly teach this course."""

        instructors = query(
            """
                SELECT instructor FROM course_ratings
                WHERE course = ? AND instructor IS NOT NULL;
            """,
            (self.id,)
        )

        if not len(instructors):
            return []
        
        return [i[0] for i in instructors]


class Grade(IntEnum):
    """
    Simply a enum for all the possible grades. 
    Its preferable to use integers in the DB.
    """
    A_PLUS  = 14
    A       = 13
    A_MINUS = 12
    B_PLUS  = 11
    B       = 10
    B_MINUS = 9
    C_PLUS  = 8
    C       = 7
    C_MINUS = 6
    D_PLUS  = 5
    D       = 4
    D_MINUS = 3
    F_PLUS  = 2
    F       = 1
    F_MINUS = 0

    @staticmethod
    def letter_to_grade(letter):
        letter_map = {
            'A+': Grade.A_PLUS,
            'A' : Grade.A,
            'A-': Grade.A_MINUS,
            'B+': Grade.B_PLUS,
            'B' : Grade.B,
            'B-': Grade.B_MINUS,
            'C+': Grade.C_PLUS,
            'C' : Grade.C,
            'C-': Grade.C_MINUS,
            'D+': Grade.D_PLUS,
            'D' : Grade.D,
            'D-': Grade.D_MINUS,
            'F+': Grade.F_PLUS,
            'F' : Grade.F,
            'F-': Grade.F_MINUS 
        }

        letter = letter.upper().strip()

        if letter not in letter_map:
            return None
        
        return letter_map[letter]
    
    @staticmethod
    def grade_to_letter(grade):
        grade = Grade.F_MINUS if grade < 0  else grade
        grade = Grade.A_PLUS  if grade > 14 else grade

        return {
            Grade.A_PLUS : 'A+',
            Grade.A      : 'A' ,
            Grade.A_MINUS: 'A-',
            Grade.B_PLUS : 'B+',
            Grade.B      : 'B' ,
            Grade.B_MINUS: 'B-',
            Grade.C_PLUS : 'C+',
            Grade.C      : 'C' ,
            Grade.C_MINUS: 'C-',
            Grade.D_PLUS : 'D+',
            Grade.D      : 'D' ,
            Grade.D_MINUS: 'D-',
            Grade.F_PLUS : 'F+',
            Grade.F      : 'F' ,
            Grade.F_MINUS: 'F-' 
        }[grade]