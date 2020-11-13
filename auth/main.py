import jwt
from http.cookies import SimpleCookie

KEY = 'mohammad'
ALGORITHM = 'HS256'


def generate_token(payload):
    encoded = jwt.encode(payload, KEY, algorithm=ALGORITHM).decode("utf-8")
    return encoded


def decode_token(token):
    decoded = jwt.decode(token, KEY, algorithm=ALGORITHM)
    return decoded


def auth_required(fn):
    from functools import wraps

    @wraps(fn)
    def inner(*args, **kwargs):
        not_allowed = False
        cookies = SimpleCookie(args[0].headers.get('Cookie'))
        username_cookie = cookies.get('username')
        token_cookie = cookies.get('user-token')
        if username_cookie:
            if token_cookie:
                token = token_cookie.value
                decoded_token = decode_token(token)
                token_username = decoded_token.get('username')
                requested_username = username_cookie.value
                not_allowed = requested_username != token_username
            else:
                not_allowed = True

        return fn(*args, **kwargs, not_allowed=not_allowed)
    return inner
