from response.requestHandler import RequestHandler


class TemplateHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'text/html'

    def getContents(self):
        return self.contents.read()

    def find(self, path):
        try:
            template_file = open('templates/{}'.format(path))
            return template_file
        except:
            return None

    def handle(self, path):
        return_template = self.find(path)
        if return_template:
            self.contents = return_template
            self.setStatus(200)
        else:
            self.setStatus(404)
