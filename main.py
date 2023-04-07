from datetime import datetime
import requests
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response, RedirectResponse, FileResponse
from starlette.routing import Route
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from ics import Calendar


import sqlite3
from sqlite3 import Error
from database.crud.AssignmentCRUD import AssignmentCRUD
from database.crud.CourseCRUD import CourseCRUD

from database.models import Assignment

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


init_db()
populate()

def context(req: Request):
    return {'assignments': AssignmentCRUD.get_all_assignments(), 
            'courses': CourseCRUD.get_all_courses_map(),
            'assignments_mapped_json': AssignmentCRUD.get_all_assignments_map(),
            'courses_mapped_json': CourseCRUD.get_all_courses_mapped_json()
    }

# Templates

templates = Jinja2Templates(directory='templates', context_processors=[context])

async def homepage(req):
    return templates.TemplateResponse('index.html', {'request': req})

async def calendar(req):
    return templates.TemplateResponse('calendar.html', {'request': req})

async def calendar_grid(req):
    return templates.TemplateResponse('calendar_grid.html', {'request': req})

async def add_assignment(req):
    return templates.TemplateResponse('add_assignment.html', {'request': req})

async def remove_assignment(req):
    return templates.TemplateResponse('remove_assignment.html', {'request': req})

async def edit_assignment(req):
    return templates.TemplateResponse('edit_assignment.html', {'request': req})

async def settings(req):
    return templates.TemplateResponse('settings.html', {'request': req})

# Endpoints

async def add_assignment_request(req: Request):
    data = await req.form()
    assignment = Assignment(0, data['course'], data['assignment_name'], 0, data['grade_weight'], 0, False, datetime.strptime(data['due_date'], '%Y-%m-%d').strftime('%Y-%m-%d'), False, None)
    AssignmentCRUD.create_assignment(assignment.params())

    return templates.TemplateResponse('add_assignment.html', {'request': req})

async def remove_assignment_request(req: Request):
    data = await req.form()
    for assignment_id in data:
        AssignmentCRUD.remove_assignment_by_id(assignment_id)
    return templates.TemplateResponse('remove_assignment.html', {'request': req})

async def edit_assignment_request(req: Request):
    # get assingment_id from req form
    data = await req.form()
    # Get first item in dict since there should only be 1 item total
    assignment_id = list(data.keys())[0]
    # Redirect to edit_assignment_single with the assignment model info we want to edit
    return templates.TemplateResponse('edit_assignment_single.html', {'request': req, 'assignment': AssignmentCRUD.get_assignment_by_id(assignment_id)})

async def edit_assignment_single_request(req: Request):
    # Apply changes
    data = await req.form()
    # Get assignment using id
    assignment = AssignmentCRUD.get_assignment_by_id(data['assignment_id'])
    assignment.name = data['assignment_name']
    assignment.course_id = data['course']
    assignment.due = datetime.strptime(data['due_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    assignment.weight = data['grade_weight']
    # completed?

    AssignmentCRUD.remove_assignment_by_id(str(assignment.id))
    AssignmentCRUD.create_assignment(assignment.params())
    # Redirect back to edit assignment selection page
    return templates.TemplateResponse('edit_assignment.html', {'request': req})


async def import_url(req: Request):
    data = await req.form()
    url = data['url']
    print(data['course'])

    cal = Calendar(requests.get(url).text)
    for event in cal.events:
        print(event.name)
        print(event.begin.datetime)

    return templates.TemplateResponse('settings.html', {'request': req})

async def import_database(req: Request):
    # Open a connection to the db file and copy everything over, 
    async with req.form() as form:
        file = form['file'].file
        with open("storage.db", "wb") as f:
            f.write(file.read())
        
    return templates.TemplateResponse('settings.html', {'request': req})

async def export_database(req: Request):
    return FileResponse('storage.db')

# Routing

app = Starlette(debug=True, routes=[
    Route('/', endpoint=homepage),
    Route('/calendar', endpoint=calendar),
    Route('/calendar_grid', endpoint=calendar_grid),
    Route('/add_assignment', endpoint=add_assignment),
    Route('/remove_assignment', endpoint=remove_assignment),
    Route('/edit_assignment', endpoint=edit_assignment),
    Route('/settings', endpoint=settings),

    Route('/add_assignment.html', endpoint=add_assignment_request, methods=['POST']),
    Route('/remove_assignment.html', endpoint=remove_assignment_request, methods=['POST']),
    Route('/edit_assignment.html', endpoint=edit_assignment_request, methods=['POST']),
    Route('/edit_assignment_single.html', endpoint=edit_assignment_single_request, methods=['POST']),
    Route('/import_url', endpoint=import_url, methods=['POST']),
    Route('/import_database', endpoint=import_database, methods=['POST']),
    Route('/database.db', endpoint=export_database, methods=['GET']),
    
    Mount('/', app=StaticFiles(directory='public')),
])
