from datetime import datetime
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response, RedirectResponse
from starlette.routing import Route
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates


import sqlite3
from sqlite3 import Error
from database.crud.AssignmentCRUD import AssignmentCRUD
from database.crud.CourseCRUD import CourseCRUD

from database.models.UserModel import UserModel
from database.models.models import Assignment

from database.pop_db import populate


def init_db():
    conn = None
    try:
        # Get our db connection
        conn = sqlite3.connect('storage.db')
        # Create our tables if they don't already exist
        # TODO: figure out length limits and fix data type/***attributes***
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username CHAR[32] UNIQUE,
            password CHAR[32],
            email CHAR[255],
            phone_number CHAR[32],
            degree CHAR[32],
            semester CHAR[32]);
        """)

        conn.execute("""CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            name CHAR[32],
            section CHAR[32],
            professor_name CHAR[32],
            online BOOL,
            dropped BOOL,
            color CHAR[6]);
        """)

        # Shouldn't weight just be based on the type of assignment?
        conn.execute("""CREATE TABLE IF NOT EXISTS assignments (
            assignment_id INTEGER PRIMARY KEY,
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
            subassignment_id INTEGER PRIMARY KEY,
            assignment_id INT,
            name CHAR[32],
            completed BOOL,
            due DATETIME,
            recurring BOOL,
            notification_id INT);
        """)

        conn.execute("""CREATE TABLE IF NOT EXISTS notifications (
            notification_id INTEGER PRIMARY KEY,
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

async def homepage(req):
    return templates.TemplateResponse('index.html', {'request': req})


init_db()
populate()

def context(req: Request):
    return {'assignments': AssignmentCRUD.get_all_assignments(), 
            'courses': CourseCRUD.get_all_courses_map(),
            'assignments_mapped_json': AssignmentCRUD.get_all_assignments_map(),
            'courses_mapped_json': CourseCRUD.get_all_courses_mapped_json()
    }

templates = Jinja2Templates(directory='templates', context_processors=[context])

async def calendar(req):
    return templates.TemplateResponse('calendar.html', {'request': req})

async def calendar_grid(req):
    return templates.TemplateResponse('calendar_grid.html', {'request': req})

async def add_assignment(req):
    return templates.TemplateResponse('add_assignment.html', {'request': req})

async def remove_assignment(req):
    pass

app = Starlette(debug=True, routes=[
    Route('/', endpoint=homepage),
    Route('/calendar', endpoint=calendar),
    Route('/calendar_grid', endpoint=calendar_grid),
    Route('/add_assignment', endpoint=add_assignment),
    Route('/remove_assignment', endpoint=remove_assignment),

    Route('/add_assignment.html', endpoint=add_assignment, methods=['POST']),
    
    Mount('/', app=StaticFiles(directory='public')),
])
