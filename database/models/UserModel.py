import sqlite3
from sqlite3 import Error


class UserModel:
  def __init__(self, user_id, username, password, email, phone_number, degree, semester):
    self.user_id = user_id
    self.username = username
    self.password = password
    self.email = email
    self.phone_number = phone_number
    self.degree = degree
    self.semester = semester

  @staticmethod
  def from_username(username):
    conn = None
    user = None
    try:
      conn = sqlite3.connect('storage.db')
      cur = conn.cursor()
      cur.execute('SELECT * FROM users WHERE username=(?)', (username,))
      user = UserModel(*cur.fetchone())
    except Error as e:
      print(e)
    finally:
      if conn:
        conn.close()
      if user:
        return user
    
    return None