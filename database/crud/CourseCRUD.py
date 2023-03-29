from dataclasses import asdict
import sqlite3
from ..models.models import Course

class CourseCRUD:
    sql_course_select_all = """
                SELECT * FROM courses
    """
    
    @staticmethod
    def get_all_courses():
        with sqlite3.connect("storage.db") as conn:
            val = conn.execute(CourseCRUD.sql_course_select_all).fetchall()
            return [Course(*i) for i in val]

    def get_all_courses_map():
        courses = CourseCRUD.get_all_courses()
        mapped_courses = {}
        for course in courses:
            mapped_courses[course.id] = course
        return mapped_courses

    def get_all_courses_mapped_json():
        courses = CourseCRUD.get_all_courses()
        mapped_courses = {}
        for course in courses:
            mapped_courses[course.id] = asdict(course)
        return mapped_courses

