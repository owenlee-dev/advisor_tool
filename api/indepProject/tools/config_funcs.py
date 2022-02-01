'''
Config file is used for:
- Cross referencing student progress with matrix for audit
- Accreditation reports
'''
import pandas as pd
import math
import os



def get_course_type(course_code):
    """
    Gets the course type

        Param:
            course_code : the course code

        Return:
            the course type of the given course
    """

    # replace the spacing and * if present
    course_code = course_code.replace("*", "")
    course_code = course_code.replace(" ", "")

    # if a course code is one of these, it means its a transfer course
    # just return the course_code as the course_type
    unassigned_course_codes = {"EXTRA", "BASSCI", "CSE-OPEN", "CSE-HSS", "TE"}

    if course_code in unassigned_course_codes:
        # because at line 91 and 92 strips the course_code off spaces, BAS SCI -> BASSCI
        # need to add the space back
        if course_code == "BASSCI":
            course_code = course_code[:3] + " " + course_code[3:]
        return course_code

    # check for replacements first
    temp = _get_replacements(course_code)
    # if a replacment is found, overwrite the course_code for the replacment code
    if temp is not None:
        course_code = temp

    course_type = _validate_tag(course_code)

    if _is_core(course_code):
        return "CORE"

    # special case for CSE-HSS courses, since they overlap with CSE-OPEN courses
    # if its an exception for either CSE-HSS or CSE-ITS, but is is not an exception for CSE-OPEN, return CSE-OPEN instead
    if course_type == "CSE-HSS" or course_type == "CSE-ITS":
        if (
            _is_exception(course_code, "CSE-ITS")
            or _is_exception(course_code, "CSE-HSS")
        ) and not _is_exception(course_code, "CSE-OPEN"):
            return "CSE-OPEN"

    # if its a valid tag and is not in the exceptions list
    if _is_exception(course_code, course_type):
        return None
    else:
        return course_type