import sqlite3


class AssignmentCRUD:
    sqlite_assignment_insert = """
                INSERT INTO 
                assignments(assignment_id, course_id, name, type, weight, priority, completed, due, recurring, notification_id) 
                VALUES(NULL,?,?,?,?,?,?,?,?,?)
            """
    
    @staticmethod
    def create_assignment(params: tuple):
        with sqlite3.connect("storage.db") as conn:
            conn.execute(AssignmentCRUD.sqlite_assignment_insert, params)
            conn.commit()