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
        try:
            # Dummy data to fill the database for testing

            USER_NUM_ENTRIES = 9
            COURSE_NUM_ENTRIES = 10
            ASSIGNMENT_NUM_ENTRIES = 15

            # USER CREATION
            user_ids = [i for i in range(1, USER_NUM_ENTRIES)]
            first_name_list = [
                "Jack",
                "Jill",
                "John",
                "Peter",
                "Matthew",
                "William",
                "Damian",
                "Brandon",
                "Nicholas",
                "Wesley",
            ]
            last_name_list = ["Smith", "John", "Jones", "Peters", "Matts", "Brown"]
            usernames = set()
            while len(usernames) < USER_NUM_ENTRIES:
                usernames.add(
                    random.choice(first_name_list) + " " + random.choice(last_name_list)
                )
            # select a random number from 1-9 4 times to create pass then add that to a list of passwords, do USER_NUM_ENTRIES times
            passwords = [
                "".join(random.choice([str(i) for i in range(1, 9)]) for _ in range(4))
                for _ in range(USER_NUM_ENTRIES)
            ]
            # selects 8 random letters and adds @gmail.com and adds to a list of emails, do USER_NUM_ENTRIES times
            emails = [
                "".join(
                    random.choice([chr(value) for value in range(ord("a"), ord("a") + 26)])
                    for _ in range(7)
                )
                + "@gmail.com"
                for _ in range(USER_NUM_ENTRIES)
            ]
            # generate a random 919 phone number and add to phone_numbers list, do USER_NUM_ENTRIES times
            phone_numbers = [
                "919"
                + "".join(random.choice([str(i) for i in range(1, 9)]) for _ in range(7))
                for _ in range(USER_NUM_ENTRIES)
            ]
            degree_list = [
                "programming",
                "business",
                "music",
                "data science",
                "cybersecurity",
            ]
            degrees = [random.choice(degree_list) for _ in range(USER_NUM_ENTRIES)]
            semester_list = ["SPR 2023", "FA 2023", "SPR 2022", "FA 2022"]
            semesters = [random.choice(semester_list) for _ in range(USER_NUM_ENTRIES)]
            dummy_user_data = zip(
                user_ids, usernames, passwords, emails, phone_numbers, degrees, semesters
            )

            # ASSIGNMENT CREATION
            course_ids = []
            for i in range(ASSIGNMENT_NUM_ENTRIES):
                course_ids.append(random.randint(1, COURSE_NUM_ENTRIES))
            assignment_names_list = [
                "Homework 1",
                "Homework 2",
                "Quiz 1",
                "Quiz 2",
                "Test 1",
                "Test 2",
            ]
            assignment_types_list = [
                "Homework",
                "Quiz",
                "Test",
                "Discussion Board",
                "Project",
                "Extra Credit",
            ]
            assignment_weights_list = [0.3, 0.25, 0.5, 0.1, 0.33]
            assignment_priorities_list = ["High", "Medium", "Low"]
            assignment_names = [
                random.choice(assignment_names_list) for _ in range(ASSIGNMENT_NUM_ENTRIES)
            ]
            assingment_types = [
                random.choice(assignment_types_list) for _ in range(ASSIGNMENT_NUM_ENTRIES)
            ]
            assignment_weights = [
                random.choice(assignment_weights_list)
                for _ in range(ASSIGNMENT_NUM_ENTRIES)
            ]
            assignment_priorities = [
                random.choice(assignment_priorities_list)
                for _ in range(ASSIGNMENT_NUM_ENTRIES)
            ]
            assignment_completed = [
                bool(random.getrandbits(1)) for _ in range(ASSIGNMENT_NUM_ENTRIES)
            ]
            # create random 2023 due dates for each assignment
            assignment_due_dates_list = [
                "2023-"
                + f"04-"
                + f"{random.choice(range(1, 29)):02}"
                for _ in range(ASSIGNMENT_NUM_ENTRIES)
            ]
            assignment_recurring = [
                bool(random.getrandbits(1)) for _ in range(ASSIGNMENT_NUM_ENTRIES)
            ]
            assignment_notification_id = [i for i in range(1, ASSIGNMENT_NUM_ENTRIES)]
            dummy_assignment_data = zip(
                # assignment_ids,
                course_ids,
                assignment_names,
                assingment_types,
                assignment_weights,
                assignment_priorities,
                assignment_completed,
                assignment_due_dates_list,
                assignment_recurring,
                assignment_notification_id,
            )

            # COURSE CREATION
            # id's generated automatically
            course_names_list = [
                "CTS-115: INFORMATION SYSTEMS BUSINESS CONCEPTS",
                "CTS-120: HARDWARE/SOFTWARE SUPPORT",
                "CTS-130: SPREADSHEET",
                "CTS-155: TECH SUPPORT FUNCTIONS",
                "CTS-220: ADVANCED HARDWARE/SOFTWARE SUPPORT",
                "DBA-120: DATABASE PROGRAMMING I",
                "DBA-130: INTRODUCTION TO NOSQL DATABASES",
                "DBA-240: DATABASE ANALYSIS AND DESIGN",
                "CSC-114: ARTIFICIAL INTELLIGENCE I",
                "CSC-120: COMPUTING FUNDAMENTALS I",
                "CSC-121: PYTHON PROGRAMMING",
                "CSC-122: PYTHON APPLICATION DEVELOPMENT",
            ]
            course_section_list = [i for i in range(1, 3)]
            professor_name_list = [
                "Chen, Chen-Pi Peter",
                "Cui, Hong",
                "Cox, George",
                "Copperthwaite, Joan A.",
                "Darvish, Ali",
                "Ellis, Charlotte D.",
                "Matlock, James L.",
                "Paul, Pamela L.",
                "Rizzo, Susan",
                "Samuels, Roslyn R.",
                "Steffes, Ryan B.",
                "Swearingen, Brad J.",
            ]
            color_list = ["FF0000", "0000FF", "FFA500", "FFC0CB", "00FF00", "FFFF00", "8F00FF"]
            # course_names = [
            #     random.choice(course_names_list) for _ in range(COURSE_NUM_ENTRIES)
            # ]
            course_names = [course_names_list[i] for i in range(COURSE_NUM_ENTRIES)]
            course_sections = [
                random.choice(course_section_list) for _ in range(COURSE_NUM_ENTRIES)
            ]
            professor_names = [
                random.choice(professor_name_list) for _ in range(COURSE_NUM_ENTRIES)
            ]
            online = [bool(random.getrandbits(1)) for _ in range(COURSE_NUM_ENTRIES)]
            dropped = [bool(random.getrandbits(1)) for _ in range(COURSE_NUM_ENTRIES)]
            colors = [random.choice(color_list) for _ in range(COURSE_NUM_ENTRIES)]
            dummy_course_data = zip(
                course_names, course_sections, professor_names, online, dropped, colors
            )

            # delete data if already present for fresh database creation
            # insert into users
            with sqlite3.connect("storage.db") as conn:
                conn.execute("DELETE FROM users")
                sqlite_user_insert = """
                    INSERT INTO 
                    users(user_id, username, password, email, phone_number, degree, semester) 
                    VALUES(?,?,?,?,?,?,?)
                """
                conn.execute(
                    sqlite_user_insert,
                    (
                        0,
                        "user",
                        "password",
                        "email@gmail.com",
                        "9198675309",
                        "programming",
                        "SPR 2023",
                    ),
                )
                for item in dummy_user_data:
                    conn.execute(sqlite_user_insert, item)
                conn.commit()

            # insert into assignments
            with sqlite3.connect("storage.db") as conn:
                conn.execute("DELETE FROM assignments")
                sqlite_assignment_insert = """
                    INSERT INTO 
                    assignments(course_id, name, type, weight, priority, completed, due, recurring, notification_id) 
                    VALUES(?,?,?,?,?,?,?,?,?)
                """
                for item in dummy_assignment_data:
                    conn.execute(sqlite_assignment_insert, item)
                conn.commit()

            with sqlite3.connect("storage.db") as conn:
                conn.execute("DELETE FROM courses")
                sqlite_course_insert = """
                    INSERT INTO
                    courses(name, section, professor_name, online, dropped, color)
                    VALUES(?,?,?,?,?,?)
                """
                for item in dummy_course_data:
                    conn.execute(sqlite_course_insert, item)
                conn.commit()
        except Error as error:
            print(error)

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
