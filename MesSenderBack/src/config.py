from os import environ

from dotenv import load_dotenv

load_dotenv()

DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")

SECRET = environ.get("SECRET")