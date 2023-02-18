import sqlite3
from sqlite3 import Error
import random

def populate():
    conn = None
    try:
        
        ### Dummy data to fill the database for testing
        
        ## USER CREATION
        NUM_ENTRIES = 9
        USER_ID_LENGTH = 9
        user_ids = [i for i in range(1, USER_ID_LENGTH)]
        first_name_list = ['Jack', 'Jill', 'John', 'Peter', 'Matthew', 'William', 'Damian', 'Brandon', 'Nicholas', 'Wesley']
        last_name_list = ['Smith', 'John', 'Jones', 'Peters', 'Matts', 'Brown']
        usernames = [random.choice(first_name_list) + ' ' + random.choice(last_name_list) for _ in range(NUM_ENTRIES)]
        # select a random number from 1-9 4 times to create pass then add that to a list of passwords, do NUM_ENTRIES times
        passwords = [''.join(random.choice([str(i) for i in range(1, 9)]) for _ in range(4)) for _ in range(NUM_ENTRIES)]
        # selects 8 random letters and adds @gmail.com and adds to a list of emails, do NUM_ENTRIES times
        emails = [''.join(random.choice([chr(value) for value in range(ord('a'), ord('a') + 26)]) for _ in range(7)) + '@gmail.com' for _ in range(NUM_ENTRIES)]
        # generate a random 919 phone number and add to phone_numbers list, do NUM_ENTRIES times
        phone_numbers = ['919' + ''.join(random.choice([str(i) for i in range(1, 9)]) for _ in range(7)) for _ in range(NUM_ENTRIES)]
        degree_list = ['programming', 'business', 'music', 'data science', 'cybersecurity']
        degrees = [random.choice(degree_list) for _ in range(NUM_ENTRIES)]
        semester_list = ['SPR 2023', 'FA 2023', 'SPR 2022', 'FA 2022']
        semesters = [random.choice(semester_list) for _ in range(NUM_ENTRIES)]
        dummy_user_data = zip(user_ids, usernames, passwords, emails, phone_numbers, degrees, semesters)
        
        ## ASSIGNMENT CREATION
        
        with sqlite3.connect('storage.db') as conn:
            sqlite_user_insert = '''
                INSERT INTO 
                users(user_id, username, password, email, phone_number, degree, semester) 
                VALUES(?,?,?,?,?,?,?)
            '''
            conn.execute(sqlite_user_insert, (0, 'mbarneto', '1234', 'email@gmail.com', '9198675309', 'programming', 'SPR 2023'))
            for item in dummy_user_data:
                conn.execute(sqlite_user_insert, item)
            conn.commit()
    except Error as error:
        print(error)