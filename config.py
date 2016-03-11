from db_config import SQLALCHEMY_DATABASE_URI

def randomkey(length):
    import random
    import string
    return ''.join(random.choice(string.lowercase) for i in range(length))

SQLALCHEMY_POOL_RECYCLE = 3600

SERVER_NAME = 'localhost:5000'
SECRET_KEY = randomkey(30)
DEBUG = True
