import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'HBJHBUGBOIH*(^&vjhsadsa7809)as')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    #SQLALCHEMY_DATABASE_URI = "mysql://root:NilArie12@localhost/database_final_project"

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    
    SQLALCHEMY_DATABASE_URI = "mysql://root:pass1nee@localhost/database_final_project"
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed)
    HOSTURL = "http://127.0.0.1:5000/"