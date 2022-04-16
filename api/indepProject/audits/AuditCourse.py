import json

class AuditCourse:
    # save memory space by defining the attributed beforehand
    __slots__ = ('course_id', 'course_type', 'credit_hours', 'grade', 'term')
    
    def __init__(self, course_id, course_type, credit_hours, grade, term):
        self.course_id=course_id
        self.course_type=course_type
        self.credit_hours = credit_hours
        self.grade = grade
        self.term = term

    def toJSON(self):
        return {
            "course_id":self.course_id,
            "course_type":self.course_type,
            "credit_hours":self.credit_hours,
            "grade":self.grade,
            "term":self.term
        }