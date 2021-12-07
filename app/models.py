from flask_login import UserMixin
from datetime import datetime
from . import db
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Products(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    stockAmount = db.Column(db.Integer)
    originalPrice = db.Column(db.Float)
    imgLink = db.Column(db.String(256), unique=True, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
