from response.requestHandler import RequestHandler
from response.templateHandler import TemplateHandler
from urllib import parse
from auth.main import generate_token
from entities.user import User


class ServiceHandler(TemplateHandler):

    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None

    def register_login(self, body):
        credential = parse.parse_qs(body, keep_blank_values=True)
        self.username = credential['username'][0]
        self.password = credential['password'][0]
        user = User.load_from_db_by_username(self.username)
        if user:
            allowed = user.auth(self.password)
        else:
            allowed = True
            new_user = User(self.username)
            new_user.set_password(self.password)
            new_user.save_to_db()

        if allowed:
            self.token = generate_token({'username': self.username})
            self.setStatus(301)
        else:
            self.setStatus(401)
