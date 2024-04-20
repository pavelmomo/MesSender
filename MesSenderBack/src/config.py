from os import environ

from dotenv import load_dotenv

load_dotenv()

DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
JWT_SECRET = environ.get("JWT_SECRET")
JWT_COOKIE_NAME = environ.get("JWT_COOKIE_NAME")
JWT_ALGORITHM = environ.get("JWT_ALGORITHM")
JWT_EXPIRATION_TIME = int(environ.get("JWT_EXPIRATION_TIME"))
MODERATOR_PASS = environ.get("MODERATOR_PASS")

