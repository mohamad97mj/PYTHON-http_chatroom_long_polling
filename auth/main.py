import jwt

KEY = 'mohammad'
ALGORITHM = 'HS256'


def generate_token(payload):
    encoded = jwt.encode(payload, KEY, algorithm=ALGORITHM).decode("utf-8")
    return encoded


def decode_token(token):
    decoded = jwt.decode(token, KEY, algorithm=ALGORITHM)
    return decoded
