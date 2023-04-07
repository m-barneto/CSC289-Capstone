import sqlite3
from sqlite3 import Error
import random


def populate():
    conn = None
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
        usernames = set([])
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
        assignment_ids = [i for i in range(1, ASSIGNMENT_NUM_ENTRIES)]
        course_ids = []
        for i in range(ASSIGNMENT_NUM_ENTRIES):
            course_ids.append(random.choice(range(COURSE_NUM_ENTRIES)))
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
            + f"03-"
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
                    "mbarneto",
                    "1234",
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
                assignments(assignment_id, course_id, name, type, weight, priority, completed, due, recurring, notification_id) 
                VALUES(NULL,?,?,?,?,?,?,?,?,?)
            """
            for item in dummy_assignment_data:
                conn.execute(sqlite_assignment_insert, item)
            conn.commit()

        with sqlite3.connect("storage.db") as conn:
            conn.execute("DELETE FROM courses")
            sqlite_course_insert = """
                INSERT INTO
                courses(course_id, name, section, professor_name, online, dropped, color)
                VALUES(NULL,?,?,?,?,?,?)
            """
            for item in dummy_course_data:
                conn.execute(sqlite_course_insert, item)
            conn.commit()
    except Error as error:
        print(error)
