import sqlite3
from sqlite3 import Error


# Encapsulates access to the sql database
class AssignmentDatabase:

    """ Default Function Section """

    # initialize function
    # formally: init_db()
    def __init__(self):
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

    # Provide default database data
    # For testing purposes only
    #
    # @todo Validate semicolon neccessity after VALUES() list
    def populate(self):
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

    # Make sure to close connection after use.
    # This is the untouched example from https://www.sqlitetutorial.net/sqlite-python/update/
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    """ Row Modification Section """
    """ ======== Adding ======== """

    # SQL pass function to add new row to USERS table
    def add_row_users(self, user_id, username, password, email, phone_number, degree, semester):
        """CREATE TABLE IF NOT EXISTS users (
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

    # SQL pass function to add new row to COURSES table
    def add_row_courses(self, course_id, name, section, professor_name, online, dropped, color):
        """CREATE TABLE IF NOT EXISTS courses (
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

    # SQL pass function to add new row to ASSIGNMENTS table
    # def add_row_assignments(self):
    #    pass
    # @todo Add default function with parameters. Overloading in Python doesn't exist and I don't want to have a bunch of different named functions doing the same thing.
    #
    # Utility function for adding another row to the assignments table using Assignment class
    def add_row_assignments(self, assignment):
        """CREATE TABLE IF NOT EXISTS assignments (
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

    # SQL pass function to add new row to SUBASSIGNMENTS table
    # def add_row_subassignments(self):
    #    pass
    # @todo Add default function with parameters. Overloading in Python doesn't exist and I don't want to have a bunch of different named functions doing the same thing.
    #
    # Utility function for adding another row to the subassignments table using Assignment class
    # SQL pass function to add new row to SUBASSIGNMENTS table
    def add_row_subassignments(self, subassignment_id, assignment):
        """CREATE TABLE IF NOT EXISTS subassignments (
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

    # SQL pass function to add new row to NOTIFICATIONS table
    def add_row_notifications(self, notification_id, message, delivery_method, send_at, assignment_id, subassignment_id):
        """CREATE TABLE IF NOT EXISTS notifications (
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

    """ Row Modification Section """
    """ ======= Removing ======= """

    # SQL pass function to remove row from to USERS table
    def remove_row_users(self, user_id):
        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM users WHERE user_id = ?
            ''', user_id)

            conn.commit()
            conn.close()

    # SQL pass function to remove row from COURSES table
    def remove_row_courses(self, course_id):
        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM courses WHERE course_id = ?
            ''', course_id)

            conn.commit()
            conn.close()

    # SQL pass function to remove row from ASSIGNMENTS table
    def remove_row_assignments(self, assignment_id):
        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM assignments WHERE assignment_id = ?
            ''', assignment_id)

            conn.commit()
            conn.close()

    # SQL pass function to remove row from SUBASSIGNMENTS table
    def remove_row_subassignments(self, subassignment_id):
        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM subassignments WHERE subassignment_id = ?
            ''', subassignment_id)

            conn.commit()
            conn.close()

    # SQL pass function to remove row from NOTIFICATIONS table
    def remove_row_notifications(self, notification_id):
        conn = self.create_connection('storage.db')
        if conn is not None:
            conn.execute('''
                DELETE FROM notifications WHERE notification_id = ?
            ''', notification_id)

            conn.commit()
            conn.close()

    """ Row Modification Section """
    """ ======= Updating ======= """

    def update_row_users(self):
        pass
    def update_row_courses(self):
        pass

    # SQL pass function to update row in ASSIGNMENTS table
    def update_row_assignments(self, assignment):
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

    # Utility function for only updating the 'recurring' column of a row
    def update_row_assignments_recurring(self, assignment):
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
