from dataclasses import asdict
import sqlite3
from ..models.models import Assignment
from datetime import datetime

class AssignmentCRUD:
    sqlite_assignment_insert = """
                INSERT INTO 
                assignments(assignment_id, course_id, name, type, weight, priority, completed, due, recurring, notification_id) 
                VALUES(NULL,?,?,?,?,?,?,?,?,?)
            """
    sql_assignment_select_completed = """
                SELECT * FROM assignments WHERE completed=TRUE
    """

    sql_assignment_select_all = """
                SELECT * FROM assignments
    """
    
    @staticmethod
    def create_assignment(params: tuple):
        with sqlite3.connect("storage.db") as conn:
            conn.execute(AssignmentCRUD.sqlite_assignment_insert, params)
            conn.commit()

    @staticmethod
    def get_all_assignments():
        with sqlite3.connect("storage.db") as conn:
            val = conn.execute(AssignmentCRUD.sql_assignment_select_all).fetchall()
            return [Assignment(*i) for i in val]
    
    @staticmethod
    def get_all_assignments_map():
        assignments = AssignmentCRUD.get_all_assignments()
        mapped_assignments = {}
        for assignment in assignments:
            mapped_assignments[assignment.id] = asdict(assignment)
        return mapped_assignments

    @staticmethod
    def get_completed_assignments():
        with sqlite3.connect("storage.db") as conn:
            val = conn.execute(AssignmentCRUD.sql_assignment_select_completed).fetchall()
            return [Assignment(*i) for i in val]

    @staticmethod
    def get_due_assignments():
        
        pass

