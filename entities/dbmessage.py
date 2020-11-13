import datetime
from db.main import CursorFromConnectionPool


class DBMessage:
    def __init__(self, src, content, date, id=None, chatroom="default"):
        self.id = id
        self.chatroom = chatroom
        self.src = src
        self.content = content
        self.date = date

    def read(self):
        self.is_read = True

    def delete(self):
        pass

    def edit(self):
        pass

    def save_to_db(self):
        # This is creating a new connection pool every time! Very expensive...
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO message (chatroom, src, content, date) VALUES (%s, %s, %s, %s)',
                           (self.chatroom, self.src, self.content, self.date))

    @classmethod
    def load_all_from_db(cls):
        with CursorFromConnectionPool() as cursor:
            # Note the (email,) to make it a tuple!
            cursor.execute('SELECT * FROM message')
            fetched_pms = []
            pms_data = cursor.fetchall()
            for pm_data in pms_data:
                fetched_pms.append(
                    DBMessage(
                        id=pm_data[0],
                        chatroom=pm_data[1],
                        src=pm_data[2],
                        content=pm_data[3],
                        date=pm_data[4],
                    ))

            return fetched_pms

    def to_dict(self):
        return {
            'id': self.id,
            'src': self.src,
            'chatroom': self.chatroom,
            'content': self.content,
            'date': self.date,
        }
