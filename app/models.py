from flask.ext.login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __unicode__(self):
        return self.username

# callback for user loading
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Room(db.Model):
    __tablename__ = 'rooms'
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique=True, index=True)
    description = db.Column(db.Text(300), index=True)

    def __init__(self, name, description):
        self.name = name
        self.description= description

    def __unicode__(self):
        return self.name