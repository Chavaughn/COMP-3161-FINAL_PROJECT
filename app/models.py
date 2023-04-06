from datetime import datetime, timedelta
from . import db
from werkzeug.security import generate_password_hash

class Account(db.Model):
    __tablename__ = 'account'

    account_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(256), unique=True)
    account_type = db.Column(db.Integer)
    def __init__(self, first_name, last_name, username, password, email, usertype):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.email = email
        self.account_type = usertype

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.account_id  # python 2 support
        except NameError:
            return self.account_id  # python 3 support

    def get_usertype(self):
        return self.user_type

    def __repr__(self):
        return '<User %r>' % (self.username)