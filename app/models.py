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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User %r>" % self.manager

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class Admin(db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, primary_key=True)
    manager = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return "<Admin %r>" % self.manager


class Cart(db.Model):
    __tablename__ = 'Cart'
    id = db.Column(db.Integer, primary_key=True)
    products_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    user_id = db.Column(db.Integer)
    number = db.Column(db.Integer, default=0)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Cart %r>" % self.id


class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    comment = db.Column(db.String(255))
    place_time = db.Column(db.DateTime, index=True, default=datetime.now)
    cdk = db.Column(db.String(255))

    def __repr__(self):
        return "<Order %r>" % self.id


class Stock(db.Model):
    __tablename__ = 'Stock'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    cdk = db.Column(db.String(255))

    def __repr__(self):
        return "<Stock %r>" % self.id