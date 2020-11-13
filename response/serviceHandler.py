from response.requestHandler import RequestHandler
from response.templateHandler import TemplateHandler
from urllib import parse


class ServiceHandler(TemplateHandler):

    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None

    def register_login(self, body):
        credential = parse.parse_qs(body, keep_blank_values=True)
        self.username = credential['username'][0]
        self.password = credential['password'][0]
        self.setStatus(301)
