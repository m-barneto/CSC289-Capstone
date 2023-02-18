import sqlite3
from sqlite3 import Error
import random


def populate():
    conn = None
    try:
        # Dummy data to fill the database for testing

        # USER CREATION
        USER_NUM_ENTRIES = 9
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
        usernames = [
            random.choice(first_name_list) + " " + random.choice(last_name_list)
            for _ in range(USER_NUM_ENTRIES)
        ]
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
        ASSIGNMENT_NUM_ENTRIES = 6
        assignment_ids = [i for i in range(1, ASSIGNMENT_NUM_ENTRIES)]
        course_ids = [i for i in range(1, ASSIGNMENT_NUM_ENTRIES)]
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
            + [f"{random.choice(str(range(1, 13))):2f}"]
            + [f"{random.choice(str(range(1, 29))):2f}"]
            for _ in range(ASSIGNMENT_NUM_ENTRIES)
        ]
        assignment_recurring = [
            bool(random.getrandbits(1)) for _ in range(ASSIGNMENT_NUM_ENTRIES)
        ]
        assignment_notification_id = [i for i in range(1, ASSIGNMENT_NUM_ENTRIES)]
        dummy_assignment_data = zip(
            assignment_ids,
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

        # insert into users
        with sqlite3.connect("storage.db") as conn:
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
            sqlite_assignment_insert = """
                INSERT INTO 
                assignments(user_id, username, password, email, phone_number, degree, semester) 
                VALUES(?,?,?,?,?,?,?,?,?,?)
            """
            for item in dummy_user_data:
                conn.execute(sqlite_assignment_insert, item)
            conn.commit()
    except Error as error:
        print(error)
