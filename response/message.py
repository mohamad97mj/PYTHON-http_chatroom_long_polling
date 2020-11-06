import time
import threading


class Message:
    def __init__(self):
        self.data = ''
        self.time = 0
        self.event = threading.Event()
        self.lock = threading.Lock()
        self.event.clear()

    def wait(self, last_mess=''):

        if self.data != last_mess and time.time()-self.time < 60:
            # resend the previous message if it is within 1 min
            return self.data
        self.event.wait()
        return self.data

    def post(self, data):
        with self.lock:
            self.data = data
            self.time = time.time()
            self.event.set()
            self.event.clear()
        return 'ok'
