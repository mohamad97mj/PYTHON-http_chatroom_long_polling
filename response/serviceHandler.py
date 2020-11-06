from response.requestHandler import RequestHandler


class ServiceHandler(RequestHandler):

    def getContents(self):
        return self.contents

    def test(self):
        self.contents = "this message is from the service"
        self.status = 200
