from entities.pm import PrivateMessage
import datetime
from db.main import CursorFromConnectionPool


class User:
    def __init__(self, username):
        self.username = username
        self.pms = None

    def receive_pm(self, new_pm):
        self.message.append(new_pm)

    def send_pm(self, dst_username, content):
        new_pm = PrivateMessage(self.username, dst_username, content, datetime.datetime.now())
        self.pms.append(new_pm)
        User.load_from_db_by_username(dst_username).receive_pm(new_pm)
        new_pm.save_to_db()

    def save_to_db(self):
        # This is creating a new connection pool every time! Very expensive...
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO user (username) VALUES (%s)', (self.username,))

    @classmethod
    def load_from_db_by_username(cls, username):
        with CursorFromConnectionPool() as cursor:
            # Note the (email,) to make it a tuple!
            cursor.execute('SELECT * FROM user WHERE username=%s', (username,))
            user_data = cursor.fetchone()
            return cls(username=user_data[0])

    @classmethod
    def load_pms_from_db_by_username(cls, username):
        with CursorFromConnectionPool() as cursor:
            # Note the (email,) to make it a tuple!
            cursor.execute('SELECT * FROM pm WHERE src=%s or dst=%s', (username, username))
            pms_data = cursor.fetchall()
            for pm_data in pms_data:
                self.pms.append(
                    PrivateMessage(
                        src=pm_data[1],
                        dst=pm_data[2],
                        content=pm_data[3],
                        date=pm_data[4],
                        id=pm_data[0],
                        is_read=pm_data[5]))
            return self.pms
