def randomkey(length):
    import random
    import string
    return ''.join(random.choice(string.lowercase) for i in range(length))

SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_DATABASE_URI = 'mysql://gojob:chungpa@localhost:3306/gojob?charset=utf8'
SERVER_NAME = 'localhost:5000'
SECRET_KEY = randomkey(30)
