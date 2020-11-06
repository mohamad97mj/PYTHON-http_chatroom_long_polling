#!/usr/bin/env python3
import time
from http.server import HTTPServer
from server import Server
from socketserver import ThreadingMixIn
from response.message import Message
from db.main import Database

ThreadingMixIn.daemon_threads = True


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


HOST_NAME = 'localhost'
PORT_NUMBER = 8000
message = None

if __name__ == '__main__':
    Database.initialise(database="chatroom", user="postgres", password="mJ604998", host="localhost", port=6000)
    httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
