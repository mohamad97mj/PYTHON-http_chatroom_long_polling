from response.requestHandler import RequestHandler
from response.templateHandler import TemplateHandler


class ServiceHandler(TemplateHandler):

    def register_login(self):
        self.setStatus(301)
