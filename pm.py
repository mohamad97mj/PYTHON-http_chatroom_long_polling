class PrivateMessage:
    def __init__(self, src, dst, content, date):
        self.src = src
        self.dst = dst
        self.content = content
        self.date = date
        self.is_read = False

    def read(self):
        self.is_read = True

    def delete(self):
        pass

    def edit(self):
        pass
