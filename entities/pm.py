import datetime
from db.main import CursorFromConnectionPool


class PrivateMessage:
    def __init__(self, src, dst, content, date, id=None, is_read=False):
        self.src = src
        self.dst = dst
        self.content = content
        self.date = date
        self.id = id
        self.is_read = is_read

    def read(self):
        self.is_read = True

    def delete(self):
        pass

    def edit(self):
        pass

    def save_to_db(self):
        # This is creating a new connection pool every time! Very expensive...
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO pm (src, dst, content, date, is_read) VALUES (%s, %s, %s, %s, %s)',
                           (self.src, self.dst, self.content, self.date, self.is_read))

    # @classmethod
    # def load_from_db_by_id(cls, id):
    #     with CursorFromConnectionPool() as cursor:
    #         # Note the (email,) to make it a tuple!
    #         cursor.execute('SELECT * FROM pm WHERE id=%s', (id,))
    #         pm_data = cursor.fetchone()
    #         return cls(src=pm_data[1], dst=pm_data[2], content=pm_data[3], date=pm_data[4], id=pm_data[0],
    #                    is_read=pm_data[5])
