import os
from typing import Tuple
from http.server import BaseHTTPRequestHandler
import socketserver

from routes.main import routes
from services.main import *
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.serviceHandler import ServiceHandler
from response.staticHandler import StaticHandler
from response.message import Message

message = Message()


class Server(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    def do_HEAD(self):
        return

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)
        service = None
        if self.path.startswith('/'):
            service = self.path[1:]
        print(service)

        if service in massage_post_services:
            res = self.perform_operation(service, body)
            if res:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                if not isinstance(res, bytes):
                    res = bytes(res, encoding='utf-8')
                self.wfile.write(res)
            else:
                self.send_response(404)
        elif service in other_post_services:
            handler = ServiceHandler()
            handler.register_login()
            self.respond({
                'handler' : handler
            })

        else:
            self.send_response(404)

    def perform_operation(self, service, body):

        if service == 'poll':
            return message.wait(body)
        elif service == 'send-message':
            return message.post(body)

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if request_extension == "" or request_extension == ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])

            elif self.path in get_services:
                handler = ServiceHandler()
                handler.test()
            else:
                handler = BadRequestHandler()

        elif request_extension == ".py":
            handler = BadRequestHandler()
        else:
            handler = StaticHandler()
            handler.find(self.path)

        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code == 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
