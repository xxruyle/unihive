from db import query
from university import University

class Department:
    def __init__(self, id, name, abbreviation, university_id):
        self.id           = id
        self.name         = name
        self.abbreviation = abbreviation
        self.university   = University.get_university_by_id(university_id)

    @staticmethod
    def get_department_by_id(id):
        params = query(
            "SELECT id, name, abbreviation, university FROM departments WHERE id = ?", 
            (id,),
            count = 1
        )
        if not params: return None
        return Department(*params)
    
    @staticmethod
    def get_department_by_abbreviation(university, abbreviation):
        params = query(
            """
                SELECT id, name, abbreviation, university FROM departments 
                WHERE university = ? AND abbreviation = ?;
            """, 
            (university.id, abbreviation.upper()),
            count = 1
        )
        if not params: return None
        return Department(*params)                      