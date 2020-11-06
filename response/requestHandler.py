class MockFile():
    def read(self):
        return False


class RequestHandler:
    def __init__(self):
        self.contentType = ""
        self.contents = MockFile()

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getContentType(self):
        return self.contentType

    def getType(self):
        return 'static'
