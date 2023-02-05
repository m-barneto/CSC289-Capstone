from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import sqlite3
from sqlite3 import Error

from database.models.UserModel import UserModel
from database.init_db import init_db
from database.pop_db import populate


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
populate()
#populate_db()
user = UserModel.from_username('mbarneto')
print(user)


app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/req', endpoint=post_req, methods=['POST']),
    Route('/req', endpoint=get_req, methods=['GET'])
])