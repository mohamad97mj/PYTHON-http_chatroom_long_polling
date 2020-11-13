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
from response.notAllowedRequestHandler import NotAllowedRequestHandler
from response.message import Message
import json
from http.cookies import SimpleCookie
import datetime
from entities.dbmessage import DBMessage
from auth.main import *

message = Message()


class Server(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    def do_HEAD(self):
        return

    @auth_required
    def do_POST(self, **kwargs):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        service = None
        if self.path.startswith('/'):
            service = self.path[1:]

        if service in massage_post_services:
            res = self.perform_operation(service, body)
            if res:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                if not isinstance(res, bytes):
                    res = bytes(res, encoding='utf-8')
                try:
                    self.wfile.write(res)
                except BrokenPipeError:
                    print("handled broken pipe error")
            else:
                self.send_response(404)
        elif service in other_post_services:
            handler = ServiceHandler()
            if service == 'register-login':
                handler.register_login(body)

            self.respond(self.handle_http(handler))

        else:
            self.send_response(404)

    def perform_operation(self, service, body):

        if service == 'poll':
            return message.wait(body)
        elif service == 'send-message':
            body = json.loads(body)
            data = self.normalize_message(body)
            dbmesssage = DBMessage(body['src'], body['content'], datetime.datetime.now())
            dbmesssage.save_to_db()
            return message.post(data)
        elif service == 'load':
            return self.load_messages()

    @auth_required
    def do_GET(self, **kwargs):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if kwargs['not_allowed']:
            handler = NotAllowedRequestHandler()
        else:
            if request_extension == "" or request_extension == ".html":
                if self.path in routes:
                    handler = TemplateHandler()
                    handler.handle(routes[self.path])

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

        self.respond(self.handle_http(handler))

    def handle_http(self, handler):
        status_code = handler.getStatus()
        self.send_response(status_code)

        if status_code == 200:
            self.send_header('Content-type', handler.getContentType())
            content = handler.getContents()
        elif status_code == 301:
            self.set_cookie({
                'user-token': handler.token,
                'username': handler.username,
            })
            self.send_header('Location', 'http://localhost:8000/chatroom')
            content = "301 Redirect"
        elif status_code == 401:
            content = "401 Unauthorized"
        elif status_code == 403:
            content = "403 Forbidden"
        else:
            content = "404 Not Found"

        self.end_headers()

        return bytes(content, 'utf-8')

    def respond(self, res):
        try:
            self.wfile.write(res)
        except BrokenPipeError:
            print("handled broken pipe error")

    def set_cookie(self, cookie_dic):
        cookie = SimpleCookie()
        for k, v in cookie_dic.items():
            cookie[k] = v
        for c in cookie.values():
            self.send_header("Set-Cookie", c.OutputString())

    def normalize_message(self, message):
        return message['src'] + ' said: ' + message['content']

    def load_messages(self):
        messages = DBMessage.load_all_from_db()
        normalized_messages = ''
        for message in messages[:len(messages)-1]:
            normalized_messages += self.normalize_message(message.to_dict()) + '<br/>'
        return normalized_messages or "admin said: enjoy chatting"

    def save_message(self):
        now = datetime.datetime.now()
