import sqlite3


class UserCRUD:
    sql_create_user = """
                INSERT INTO 
                users(user_id, username, password, email, phone_number, degree, semester) 
                VALUES(?,?,?,?,?,?,?)
            """

    @staticmethod
    def create_user(params: tuple):
        with sqlite3.connect("storage.db") as conn:
            conn.execute(UserCRUD.sql_create_user, params)
            conn.commit()
