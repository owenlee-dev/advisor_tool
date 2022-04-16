import json

class Audit:
    # save memory space by defining the attributed beforehand
    __slots__ = ('courses_taken', 'courses_needed','course_type_taken', 'course_type_needed')
    
    def __init__(self, courses_taken, courses_needed,course_type_taken, course_type_needed):
        self.courses_taken=courses_taken
        self.courses_needed = courses_needed
        self.course_type_taken={}
        self.course_type_needed={}

    def toJSON(self):
       
        courses_taken_JSON={}
        for course in self.courses_taken:
            courses_taken_JSON[course.course_id]=course.toJSON()

        courses_needed_JSON={}
        for course in self.courses_needed:
            courses_needed_JSON[course]=self.courses_needed[course]
        audit={
            "courses_taken":courses_taken_JSON,
            "courses_needed":courses_needed_JSON,
            "course_type_taken": self.course_type_taken,
            "course_type_needed": self.course_type_needed
        }
        return audit   