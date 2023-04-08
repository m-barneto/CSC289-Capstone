from datetime import datetime
import requests
from starlette.applications import Starlette
from starlette.responses import Response, RedirectResponse, FileResponse
from starlette.routing import Route
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser, requires
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.templating import Jinja2Templates
from ics import Calendar
import base64
import binascii

import sqlite3
from sqlite3 import Error
from database.crud.AssignmentCRUD import AssignmentCRUD
from database.crud.CourseCRUD import CourseCRUD

from database.models import Assignment, Course

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

async def homepage(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@requires('authenticated', redirect='login')
async def assignments(request: Request):
    return templates.TemplateResponse('assignments.html', {'request': request})

@requires('authenticated', redirect='login')
async def calendar(request: Request):
    return templates.TemplateResponse('calendar.html', {'request': request})

@requires('authenticated', redirect='login')
async def add_assignment(request: Request):
    return templates.TemplateResponse('add_assignment.html', {'request': request})

@requires('authenticated', redirect='login')
async def remove_assignment(request: Request):
    return templates.TemplateResponse('remove_assignment.html', {'request': request})

@requires('authenticated', redirect='login')
async def edit_assignment(request: Request):
    return templates.TemplateResponse('edit_assignment.html', {'request': request})

@requires('authenticated', redirect='login')
async def settings(request: Request):
    return templates.TemplateResponse('settings.html', {'request': request})

# Endpoints

@requires('authenticated', redirect='login')
async def add_assignment_request(request: Request):
    data = await request.form()
    assignment = Assignment(0, data['course'], data['assignment_name'], 0, data['grade_weight'], 0, False, datetime.strptime(data['due_date'], '%Y-%m-%d').strftime('%Y-%m-%d'), False, None)
    AssignmentCRUD.create_assignment(assignment.params())

    return templates.TemplateResponse('add_assignment.html', {'request': request})

@requires('authenticated', redirect='login')
async def remove_assignment_request(request: Request):
    data = await request.form()
    for assignment_id in data:
        AssignmentCRUD.remove_assignment_by_id(assignment_id)
    return templates.TemplateResponse('remove_assignment.html', {'request': request})

@requires('authenticated', redirect='login')
async def edit_assignment_request(request: Request):
    # get assingment_id from req form
    data = await request.form()
    # Get first item in dict since there should only be 1 item total
    assignment_id = list(data.keys())[0]
    # Redirect to edit_assignment_single with the assignment model info we want to edit
    return templates.TemplateResponse('edit_assignment_single.html', {'request': request, 'assignment': AssignmentCRUD.get_assignment_by_id(assignment_id)})

@requires('authenticated', redirect='login')
async def edit_assignment_single_request(request: Request):
    # Apply changes
    data = await request.form()
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
    return templates.TemplateResponse('edit_assignment.html', {'request': request})

@requires('authenticated', redirect='login')
async def import_url(request: Request):
    data = await request.form()
    url = data['url']

    cal = Calendar(requests.get(url).text)
    for event in cal.events:
        assignment = Assignment(0, data['course'], event.name, '', '1', 0, False, event.begin.datetime.strftime('%Y-%m-%d'), False, 0)
        AssignmentCRUD.create_assignment(assignment.params())

    return templates.TemplateResponse('settings.html', {'request': request})

@requires('authenticated', redirect='login')
async def import_database(request: Request):
    # Open a connection to the db file and copy everything over, 
    async with request.form() as form:
        file = form['file'].file
        with open("storage.db", "wb") as f:
            f.write(file.read())
        
    return templates.TemplateResponse('settings.html', {'request': request})

@requires('authenticated', redirect='login')
async def export_database(request: Request):
    return FileResponse('storage.db')

@requires('authenticated', redirect='login')
async def add_course(request: Request):
    data = await request.form()
    course_name = data['course_name']
    course = Course(0, course_name, '', '', False, False, '#FF00FF')
    CourseCRUD.create_course(course.params())
    
    return templates.TemplateResponse('settings.html', {'request': request})


@requires('authenticated', redirect='login')
async def remove_course(request: Request):
    data = await request.form()
    course_id = data['course_id']
    CourseCRUD.remove_course_by_id(course_id)
    AssignmentCRUD.remove_assignments_by_course_id(course_id)
    return templates.TemplateResponse('settings.html', {'request': request})


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")

        with sqlite3.connect("storage.db") as db:
            result = db.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()

        if result is not None:
            return AuthCredentials(["authenticated"]), SimpleUser(username)


async def login(request: Request) -> Response:
    if request.user.is_authenticated:
        next_url = request.query_params.get("next")
        if next_url:
            return RedirectResponse(next_url)
        return RedirectResponse("/")
    else:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response


# Routing
middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = Starlette(debug=True, middleware=middleware, routes=[
    Route('/', endpoint=homepage),
    Route('/assignments', endpoint=assignments),
    Route('/calendar', endpoint=calendar),
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
    
    Route('/add_course', endpoint=add_course, methods=['POST']),
    Route('/remove_course', endpoint=remove_course, methods=['POST']),
    Route("/login", endpoint=login),
    
    Mount('/', app=StaticFiles(directory='public')),
])
