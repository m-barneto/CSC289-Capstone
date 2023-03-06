import sqlite3
from sqlite3 import Error


class AssignmentDatabase:
    """Encapsulates access to the sql database."""

    """
    Function Section
    ======= Defaults =======
    """

    def __init__(self):
        """
        Constructor function for AssignmentDatabase.
        Formally, init_db() was used and this class replaces that function
        As well as provides utility for access to the SQL database.
        """

        conn = self.create_connection('storage.db')
        if conn is not None:
            # Create our tables if they don't already exist
            # TODO: figure out length limits and fix data type/***attributes***
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY,
                username CHAR[32] UNIQUE,
                password CHAR[32],
                email CHAR[255],
                phone_number CHAR[32],
                degree CHAR[32],
                semester CHAR[32]);
            """)

            conn.execute("""CREATE TABLE IF NOT EXISTS courses (
                course_id INT NOT NULL PRIMARY KEY,
                name CHAR[32],
                section CHAR[32],
                professor_name CHAR[32],
                online BOOL,
                dropped BOOL,
                color CHAR[6]);
            """)

            # Shouldn't weight just be based on the type of assignment?
            conn.execute("""CREATE TABLE IF NOT EXISTS assignments (
                assignment_id INT NOT NULL PRIMARY KEY,
                course_id INT,
                name CHAR[32],
                type CHAR[32],
                weight CHAR[32],
                priority INT,
                completed BOOL,
                due DATETIME,
                recurring BOOL,
                notification_id INT);
            """)

            conn.execute("""CREATE TABLE IF NOT EXISTS subassignments (
                subassignment_id INT NOT NULL PRIMARY KEY,
                assignment_id INT,
                name CHAR[32],
                desc TEXT,
                completed BOOL,
                due DATETIME,
                recurring BOOL,
                notification_id INT);
            """)

            conn.execute("""CREATE TABLE IF NOT EXISTS notifications (
                notification_id INT NOT NULL PRIMARY KEY,
                message TEXT,
                delivery_method INT,
                send_at DATETIME,
                assignment_id INT,
                subassignment_id INT);
            """)

            conn.close()

    def populate(self):
        """
        Provide default database data.
        For testing purposes only.
        """

        conn = self.create_connection('storage.db')
        if conn is not None:
            # Should there be a semicolon after the VALUES() list?
            conn.execute('''
                INSERT INTO 
                users(user_id, username, password, email, phone_number, degree, semester) 
                VALUES(?,?,?,?,?,?,?)
            ''', (0, 'mbarneto', '1234', 'email@gmail.com', '9198675309', 'programming', 'SPR 2023'))

            conn.commit()
            conn.close()

    def create_connection(self, db_file): # This is the untouched example from https://www.sqlitetutorial.net/sqlite-python/update/
        """
        Create a database connection to the SQLite database specified by the db_file.
        Make sure to close connection after use.

        Parameters:
            db_file (string): path to directory of the database file

        Returns:
            Connection object or None
        """

        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    """
    Row Modification Section
    ====== Retrieving ======
    """

    def get_all_rows_assignments(self):
        """SELECTs all rows from the ASSIGNMENTS table."""

        rows = list()
        conn = self.create_connection('storage.db')
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM assignments
            ''')
            records = cursor.fetchall()
            for row in records:
                rows.append(row)
            conn.close()
        return rows

    def get_row_assignments(self, assignment_id):
        """SELECTs the row from the ASSIGNMENTS table with the same id."""

        row = None
        conn = self.create_connection('storage.db')
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM assignments WHERE assignment_id = ?
            ''')
            row = cursor.fetchone()
            conn.close()
        return row

    def get_all_rows_notifications(self):
        """SELECTs all rows from the NOTIFICATIONS table."""

        rows = list()
        conn = self.create_connection('storage.db')
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM notifications
            ''')
            records = cursor.fetchall()
            for row in records:
                rows.append(row)
            conn.close()
        return rows

    def get_row_notifications(self, notification_id):
        """SELECTs the row for the NOTIFICATIONS table with the same id."""

        row = None
        conn = self.create_connection('storage.db')
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM notifications WHERE notification_id = ?
            ''')
            row = cursor.fetchone()
            conn.close()
        return row

    """
    Row Modification Section
    ======== Adding ========
    """

    def add_row_users(self, user_id, username, password, email, phone_number, degree, semester):
        """
        SQL pass function to add new row to USERS table.

        CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY,
                username CHAR[32] UNIQUE,
                password CHAR[32],
                email CHAR[255],
                phone_number CHAR[32],
                degree CHAR[32],
                semester CHAR[32]);
        """

        conn = self.create_connection('storage.db')
        if conn is not None:
            # Should there be a semicolon after the VALUES() list?
            conn.execute('''
                INSERT INTO 
                users(user_id, username, password, email, phone_number, degree, semester) 
                VALUES(?,?,?,?,?,?,?)
            ''', (user_id, username, password, email, phone_number, degree, semester))

            conn.commit()
            conn.close()

    def add_row_courses(self, course_id, name, section, professor_name, online, dropped, color):
        """
        SQL pass function to add new row to COURSES table.

        CREATE TABLE IF NOT EXISTS courses (
                course_id INT NOT NULL PRIMARY KEY,
                name CHAR[32],
                section CHAR[32],
                professor_name CHAR[32],
                online BOOL,
                dropped BOOL,
                color CHAR[6]);
        """

        conn = self.create_connection('storage.db')
        if conn is not None:
            # Should there be a semicolon after the VALUES() list?
            conn.execute('''
                INSERT INTO 
                users(course_id, name, section, professor_name, online, dropped, color) 
                VALUES(?,?,?,?,?,?,?)
            ''', (course_id, name, section, professor_name, online, dropped, color))

            conn.commit()
            conn.close()

    def add_row_assignments(self, assignment):
        """
        SQL pass function to add new row to ASSIGNMENTS table

        CREATE TABLE IF NOT EXISTS assignments (
                assignment_id INT NOT NULL PRIMARY KEY,
                course_id INT,
                name CHAR[32],
                type CHAR[32],
                weight CHAR[32],
                priority INT,
                completed BOOL,
                due DATETIME,
                recurring BOOL,
                notification_id INT);
        """

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                INSERT INTO 
                assignments(assignment_id, course_id, name, type, weight, priority, completed, due, recurring, notification_id) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?)
            ''', (assignment.get_id(),
                  assignment.get_course_id(),
                  assignment.get_name(),
                  assignment.get_type(),
                  assignment.get_weight(),
                  assignment.get_priority(),
                  assignment.get_completed(),
                  assignment.get_due(),
                  assignment.get_recurring(),
                  assignment.get_notification_id()
                  ))

            conn.commit()
            conn.close()

    def add_row_subassignments(self, subassignment_id, assignment):
        """
        SQL pass function to add new row to SUBASSIGNMENTS table

        CREATE TABLE IF NOT EXISTS subassignments (
                subassignment_id INT NOT NULL PRIMARY KEY,
                assignment_id INT,
                name CHAR[32],
                desc TEXT,
                completed BOOL,
                due DATETIME,
                recurring BOOL,
                notification_id INT);
        """

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                INSERT INTO 
                subassignments(subassignment_id, assignment_id, course_id, name, type, weight, priority, completed, due, recurring, notification_id) 
                VALUES(?,?,?,?,?,?,?,?,?,?)
            ''', (subassignment_id,
                  assignment.get_id(),
                  assignment.get_course_id(),
                  assignment.get_name(),
                  assignment.get_type(),
                  assignment.get_weight(),
                  assignment.get_priority(),
                  assignment.get_completed(),
                  assignment.get_due(),
                  assignment.get_recurring(),
                  assignment.get_notification_id()
                  ))

            conn.commit()
            conn.close()

    def add_row_notifications(self, notification_id, message, delivery_method, send_at, assignment_id, subassignment_id):
        """
        SQL pass function to add new row to NOTIFICATIONS table

        CREATE TABLE IF NOT EXISTS notifications (
                notification_id INT NOT NULL PRIMARY KEY,
                message TEXT,
                delivery_method INT,
                send_at DATETIME,
                assignment_id INT,
                subassignment_id INT);
        """

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                INSERT INTO 
                assignments(notification_id, message, delivery_method, send_at, assignment_id, subassignment_id) 
                VALUES(?,?,?,?,?,?)
            ''', (notification_id, message, delivery_method, send_at, assignment_id, subassignment_id))

            conn.commit()
            conn.close()

    """ 
    Row Modification Section 
    ======= Removing ======= 
    """

    def remove_row_users(self, user_id):
        """SQL pass function to remove row from USERS table."""

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM users WHERE user_id = ?
            ''', user_id)

            conn.commit()
            conn.close()

    def remove_row_courses(self, course_id):
        """SQL pass function to remove row from COURSES table."""

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM courses WHERE course_id = ?
            ''', course_id)

            conn.commit()
            conn.close()

    def remove_row_assignments(self, assignment_id):
        """SQL pass function to remove row from ASSIGNMENTS table."""

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM assignments WHERE assignment_id = ?
            ''', assignment_id)

            conn.commit()
            conn.close()

    def remove_row_subassignments(self, subassignment_id):
        """SQL pass function to remove row from SUBASSIGNMENTS table."""

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM subassignments WHERE subassignment_id = ?
            ''', subassignment_id)

            conn.commit()
            conn.close()

    def remove_row_notifications(self, notification_id):
        """SQL pass function to remove row from NOTIFICATIONS table."""

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM notifications WHERE notification_id = ?
            ''', notification_id)

            conn.commit()
            conn.close()

    """
    Row Modification Section
    ======= Updating =======
    """

    def update_row_users(self):
        pass
    def update_row_courses(self):
        pass

    def update_row_assignments(self, assignment):
        """SQL pass function to update row in ASSIGNMENTS table."""

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                UPDATE assignments
                SET course_id = ?, 
                    name = ?, 
                    type = ?, 
                    weight = ?, 
                    priority = ?, 
                    completed = ?, 
                    due = ?, 
                    recurring = ?, 
                    notification_id = ?
                WHERE assignment_id = ?
            ''', (assignment.get_course_id(),
                  assignment.get_name(),
                  assignment.get_type(),
                  assignment.get_weight(),
                  assignment.get_priority(),
                  assignment.get_completed(),
                  assignment.get_due(),
                  assignment.get_recurring(),
                  assignment.get_notification_id(),
                  assignment.get_id()
                  ))

            conn.commit()
            conn.close()

    def update_row_assignments_recurring(self, assignment):
        """Utility function for only updating the 'recurring' column of a row."""

        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                UPDATE assignments
                SET recurring = ?
                WHERE assignment_id = ?
            ''', (assignment.get_recurring(),
                  assignment.get_id()
                  ))

            conn.commit()
            conn.close()

    def update_row_subassignments(self):
        pass
    def update_row_notifications(self):
        pass
