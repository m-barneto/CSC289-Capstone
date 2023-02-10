import datetime

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import sqlite3
from sqlite3 import Error

from database.models.UserModel import UserModel


def init_db():
    conn = None
    try:
        # Get our db connection
        conn = sqlite3.connect('storage.db')
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

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def populate_db():
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


async def homepage(request):
    return JSONResponse({'hello': 'world'})


async def get_req(req):
    return JSONResponse({'aaaaaa': 'bbbbbbbbb'})


async def post_req(req):
    return JSONResponse({'cccc': 'ddddddd'})


init_db()
populate_db()
user = UserModel.from_username('mbarneto')
print(user)

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/req', endpoint=post_req, methods=['POST']),
    Route('/req', endpoint=get_req, methods=['GET'])
])


def create_class():
    courseId = 0
    className = ""
    section = ""
    professor_name = ""
    online = False
    dropped = False
    color = ""
    # Insert links to HTML input here
    con = sqlite3.connect('storage.db')
    query = courseId, className, section, professor_name, online, dropped, color
    con.execute("INSERT INTO courses VALUES(?, ?, ?, ?, ?, ?, ?)", query)
    con.commit()


def create_assignment():
    assignmentId = 0
    courseId = 0
    name = ""
    type1 = ""
    weight = ""
    priority = 0
    completed = False
    due = datetime.today()
    recurring = False
    notificationId = 0
    # Insert links to HTML input here
    con = sqlite3.connect('storage.db')
    query = assignmentId, courseId, name, type1, weight, priority, completed, due, recurring, notificationId
    con.execute("INSERT INTO assignments VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", query)
    con.commit()


def create_subassignment():
    subassignmentId = 0
    assignmentId = 0
    name = ""
    desc = ""
    completed = False
    due = datetime.today()
    recurring = False
    notificationId = 0
    # Insert links to HTML input here
    con = sqlite3.connect('storage.db')
    query = subassignmentId, assignmentId, name, desc, completed, due, recurring, notificationId
    con.execute("INSERT INTO subassignment VALUES(?, ?, ?, ?, ?, ?, ?, ?)", query)
    con.commit()


def create_notification():
    notificationId = 0
    message = ""
    deliveryMethod = 0
    sendAt = datetime.today()
    assignmentId = 0
    subassignmentId = 0
    # Insert links to HTML input here
    con = sqlite3.connect('storage.db')
    query = notificationId, message, deliveryMethod, sendAt, assignmentId, subassignmentId
    con.execute("INSERT INTO courses VALUES(?, ?, ?, ?, ?, ?)", query)
    con.commit()
