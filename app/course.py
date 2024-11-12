# Filename: course.py
# Description: This module contains course related objects and methods
# Inputs: N/A
# Output: N/A
# Authors: Xavier Ruyle, Andrew Ward
# Creation Date: 10/24/2024

from enum import IntEnum

from course import *
from db import query
from department import Department
from university import University

COURSE_PARAMS = "courses.id, courses.name, description, course_number, department, courses.university"

class Course:
    def __init__(self, id, name, description, course_number, department_id, university_id):
        self.id             = id            # database id
        self.name           = name          # Ex: Software Engineering
        self.description    = description   # Ex: An introduction to software
        self.course_number  = course_number # Ex: 581
        self.department     = Department.get_department_by_id(department_id) # Department
        self.university     = University.get_university_by_id(university_id) # University

        # Full name, Ex: EECS-581
        self.name_combined = self.department.name + "-" + str(self.course_number)
        self.sort_post_type = "Date Created" # default sort type 

    @property
    def posts(self):
        """
        Posts belong to course getter.
        Returns list of posts in course.
        """

        # Avoid circular import.
        from post import Post

        if self.sort_post_type == "Date Created":
            sort_by = "created"   
        else: 
            sort_by = "created" 

        query_str = f"""
                SELECT id, created, title, content, author, course FROM posts
                WHERE course = ? AND parent IS NULL
                ORDER BY {sort_by};
            """

        # Return a list of all posts that aren't replies.
        return [Post(*params) for params in query(
            query_str,
            (self.id,)
        )]

    @property
    def average_difficulty(self):
        """Average difficulty of course getter."""

        # Get all the difficulties that have
        # been submitted in course ratings.
        difficulties = query(
            """
                SELECT difficulty FROM course_ratings
                WHERE course = ? AND difficulty IS NOT NULL;
            """,
            (self.id,)
        )

        # If there haven't been any entries
        # for difficulty, then return None.
        if not len(difficulties):
            return None

        # Return the average difficulty across all ratings.
        return sum(i[0] for i in difficulties) / len(difficulties)


    @property
    def average_grade(self):
        """Average grade of course getter."""

        # Get all the grade ints that have
        # been submitted in course ratings.
        grades = query(
            """
                SELECT grade FROM course_ratings
                WHERE course = ? AND grade IS NOT NULL;
            """,
            (self.id,)
        )

        # If there haven't been any entries
        # for grade value, then return None.
        if not len(grades):
            return None

        # Get the average grade across all entries.
        mean = sum(i[0] for i in grades) / len(grades)

        # Cast the result to a Grade enum.
        return Grade(round(mean))

    @property
    def credit_hours(self):
        """Mode credit hours of course getter."""


        # Get all the credit hours that have
        # been submitted in course ratings.
        hours = query(
            """
                SELECT hours FROM course_ratings
                WHERE course = ? AND hours IS NOT NULL;
            """,
            (self.id,)
        )

        # If there haven't been any entries
        # for credit hours, then return None.
        if not len(hours):
            return None

        hour_table = {}                         # Create frequency map
        for submission in hours:                # For each submission,
            if submission[0] in hour_table:     # If already in the table,
                hour_table[submission[0]] += 1  # Increment the frequency
            else:                               # Otherwise, new value
                hour_table[submission[0]] = 1   # Set the frequency to one

        # Get the mode of credit_hours. Presumably,
        # the mode will be the "correct" value.
        return max(hour_table, key = lambda x: hour_table[x])

    @property
    def instructors(self) -> list[str]:
        """Instructors that supposedly teach this course."""

        # Get all the instructors that have
        # been submitted in course ratings.
        instructors = query(
            """
                SELECT instructor FROM course_ratings
                WHERE course = ? AND instructor IS NOT NULL;
            """,
            (self.id,)
        )

        # If there haven't been any entries
        # for instructors return empty list.
        if not len(instructors):
            return []

        # Deconstruct the query array to strings.
        return [i[0] for i in instructors]

    @staticmethod
    def get_course_by_id(id: int):
        """
        Get a course by its database id.
        Return None if course not found.
        """

        params = query(
            f"SELECT {COURSE_PARAMS} FROM courses WHERE id = ?",
            (id,),
            count = 1
        )
        if not params: return None # Course not found
        return Course(*params)     # Construct course object

    @staticmethod
    def get_course_by_name_combined(university: University, name_combined: str):
        """
        Get a course by its full "combined" name (e.g. EECS-581).

        :param university: University that the course belongs to.
        :param name_combined: Combined name of course (ex: EECS-581)
        :returns: Course object or None if course not found.
        """

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
        if not params: return None # Course not found
        return Course(*params)     # Construct course object

    @staticmethod
    def get_course_by_name(university: University, name: str):
        """
        Get a course by its vernacular name (e.g. Software Engineering II).

        :param university: University that the course belongs to.
        :param name: Name of the course (ex: Software Engineering II)
        :returns: Course object or None if course not found.
        """

        params = query(
            f"SELECT {COURSE_PARAMS} FROM courses WHERE name = ? AND university = ?",
            (name, university.id),
            count = 1
        )
        if not params: return None # Course not found
        return Course(*params)     # Construct course object

    @staticmethod
    def get_course_by_course_number(university: University, department: Department, course_number: int):
        """
        Get a course by its department and number (e.g. 581).

        :param university: University that the course belongs to.
        :param department: Department that the course belongs to.
        :param course_number: Number of the course (ex: 581)
        :returns: Course object or None if course not found.
        """

        params = query(
            f"""
                SELECT {COURSE_PARAMS} FROM courses
                WHERE university = ? AND department = ? AND course_number = ?;
            """,
            (university.id, department.id, course_number),
            count = 1
        )
        if not params: return None # Course not found
        return Course(*params)     # Construct course object

    def store_info(self, user: 'User', difficulty: float = None, grade: 'Grade' = None, credit_hours: int = None, instructor: str = None):
        """
        Takes a difficulty, grade, credit hours, and an instructor
        and inserts them into the database. Note that each user can
        only have a single submission per course. If the submission
        is a  duplicate, the old submission will be modified.

        :param user: The user that is inserting information.
        :param difficulty: The difficulty of the course (1-10).
        :param grade: The grade the user received.
        :param credit_hours: The credit hours of the course.
        :param instructor: The name of the course's professor.
        """

        # Check if the user has already submitted
        # information for this particular course.
        user_already_submitted = bool(query(
            """
                SELECT * FROM course_ratings
                WHERE user = ? AND course = ?;
            """,
            (user.id, self.id),
            count = 1
        ))

        if user_already_submitted:
            # If the user has submitted info to this course
            # before, we modify their existing information.
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

            # also have to store inside course  (yeah this is bad)
            # query(
            #     """
            #         UPDATE courses SET
            #             hours      = COALESCE(?, hours),
            #         WHERE user = ? AND course = ?;
            #     """,
            #     (credit_hours, user.id, self.id)
            # )
        else:
            # Otherwise, if this is the first time,
            # we create a new entry for their info.
            query(
                """
                    INSERT INTO course_ratings (user, course, difficulty, grade, hours, instructor)
                    VALUES (?, ?, ?, ?, ?, ?);
                """,
                (user.id, self.id, difficulty, grade, credit_hours, instructor)
            )




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
    def letter_to_grade(letter: str):
        """Convert character to Grade enum."""

        # Initialize letter map table.
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

        # Cleanup the string input.
        letter = letter.upper().strip()

        # If the letter is not in the
        # map, simply return None.
        if letter not in letter_map:
            return None

        # Return the letter mapping.
        return letter_map[letter]

    @staticmethod
    def grade_to_letter(grade: 'Grade'):
        """Convert Grade enum to human-readable letter grade (ex: A+)."""

        # Enforce bounding on the input (in case its integer).
        grade = Grade.F_MINUS if grade < 0  else grade
        grade = Grade.A_PLUS  if grade > 14 else grade

        # Apply the mapping to the input.
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
