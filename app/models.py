from sqlalchemy.orm import defaultload
from app import login
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash #password hashing 
from flask_login import UserMixin


# user loaderfunction
@login.user_loader
def load_user(id):
    '''user loaderfunction, when called returns user given the ID'''
    return User.query.get(int(id))

# this model defines the initial db schema
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(160))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f"User: {self.username} email: {self.email} profile_pic: { self.image_file }")

    #passwd hashing methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
