import os

from response.requestHandler import RequestHandler


class StaticHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.filetypes = {
            ".js": "text/javascript",
            ".css": "text/css",
            ".jpg": "image/jpeg",
            ".png": "image/png",
            "notfound": "text/plain"
        }

    def find(self, file_path):
        split_path = os.path.splitext(file_path)
        extension = split_path[1]

        try:

            if extension in (".jpg", ".jpeg", ".png"):
                self.contents = open(file_path[1:], 'rb')
            else:
                self.contents = open(file_path[1:], 'r')

            self.setContentType(extension)
            self.setStatus(200)
            return True
        except:
            self.setContentType('notfound')
            self.setStatus(404)
            return False

    def setContentType(self, ext):
        self.contentType = self.filetypes[ext]

    def getContents(self):
        return self.contents.read()
