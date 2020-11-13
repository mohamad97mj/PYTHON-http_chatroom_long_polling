import json
from urllib import parse


# s = '{"key1":"value1", "key2":"value2"}'
# d = json.loads(s)
# print(d)
# print(type(d))
a = 'username=mohamad97mj&password='
b = parse.parse_qs(a, keep_blank_values=True)
print(b)