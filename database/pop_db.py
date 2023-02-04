import sqlite3
from sqlite3 import Error

def populate():
    conn = None
    try:
        conn = sqlite3.connect('storage.db')
        conn.execute('''
            INSERT INTO 
            users(user_id, username, password, email, phone_number, degree, semester) 
            VALUES(?,?,?,?,?,?,?)
        ''', (0, 'mbarneto', '1234', 'email@gmail.com', '9198675309', 'programming', 'SPR 2023'))
        
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()