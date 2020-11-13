from entities.dbmessage import DBMessage
import datetime
from db.main import CursorFromConnectionPool
import hashlib


class User:
    def __init__(self, username):
        self.username = username
        self.password = None

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    def auth(self, entered_password):
        hashed_entered_password = hashlib.sha256(entered_password.encode("utf-8")).hexdigest()
        if hashed_entered_password == self.password:
            return True
        else:
            return False

    def receive_pm(self, new_pm):
        self.message.append(new_pm)

    def send_pm(self, dst_username, content):
        new_pm = DBMessage(self.username, dst_username, content, datetime.datetime.now())
        self.pms.append(new_pm)
        User.load_from_db_by_username(dst_username).receive_pm(new_pm)
        new_pm.save_to_db()

    def save_to_db(self):
        # This is creating a new connection pool every time! Very expensive...
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO public.user (username, password) VALUES (%s, %s)', (self.username, self.password))

    @classmethod
    def load_from_db_by_username(cls, username):
        with CursorFromConnectionPool() as cursor:
            # Note the (email,) to make it a tuple!
            cursor.execute('SELECT * FROM public.user WHERE username=%s', (username,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(username=user_data[0])
            else:
                return None

