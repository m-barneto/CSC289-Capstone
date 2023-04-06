from dataclasses import asdict
import sqlite3
from ..models import Assignment
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

    sql_assignment_due_date_week = """
                SELECT * FROM assignments WHERE due BETWEEN ? AND ?
    """

    sql_delete_assignment_by_id = """
                DELETE FROM assignments WHERE assignment_id=?
    """

    sql_get_assignment_by_id = """
                SELECT * FROM assignments WHERE assignment_id=?
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
        now = datetime.date.today()
        then = datetime.date.today() + datetime.timedelta(days=7)
        with sqlite3.connect("storage.db") as conn:
            val = conn.execute(AssignmentCRUD.sql_assignment_due_date_week, now, then).fetchall()
            return [Assignment(*i) for i in val]

    @staticmethod
    def remove_assignment_by_id(assignment_id):
        with sqlite3.connect("storage.db") as conn:
            conn.execute(AssignmentCRUD.sql_delete_assignment_by_id, assignment_id)

    @staticmethod
    def get_assignment_by_id(assignment_id):
        with sqlite3.connect("storage.db") as conn:
            val = conn.execute(AssignmentCRUD.sql_get_assignment_by_id, assignment_id).fetchall()
            return [Assignment(*i) for i in val][0]
