import importlib
import subprocess
# Install required packages from requirements.txt
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
#Comment out this line once it finished ^

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from .config import Config
from flask_migrate import Migrate
import os


# import flask migrate here
app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.abspath('./uploads/')
db = SQLAlchemy(app)
with app.app_context():
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            db.create_all()
migrate = Migrate(app, db)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views

# Import all controllers in the controllers folder
controllers_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controllers')
for file_name in os.listdir(controllers_dir):
    if file_name.endswith('.py') and not file_name.startswith('__'):
        module_name = f"app.controllers.{file_name[:-3]}"
        importlib.import_module(module_name)
