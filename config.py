import os

from dotenv import load_dotenv, find_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(find_dotenv())

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No secret key set for Flask application")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WORKING_FOLDER = os.getcwd()
    INVOICE_FOLDER = 'Invoices'
    ID_FOLDER = 'ID'
    if os.environ.get("REMEMBER_COOKIE_DOMAIN"):
        REMEMBER_COOKIE_DOMAIN = os.environ.get("REMEMBER_COOKIE_DOMAIN")

    if os.environ.get("SESSION_COOKIE_DOMAIN"):
        SESSION_COOKIE_DOMAIN = os.environ.get("SESSION_COOKIE_DOMAIN")
