import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

basedir = os.path.abspath(os.path.dirname(__file__))

flask_app = Flask(__name__)
flask_app.config.update(dict(
    SECRET_KEY='SECRET_KEY',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'data.sqlite'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=True,
    MAIL_SERVER='smtp.qq.com',
    MAIL_PORT=25,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='1141252977@qq.com',
    MAIL_PASSWORD='vpwimfstnxacjhjf',
))

mail = Mail(flask_app)
bootstrap = Bootstrap(flask_app)
moment = Moment(flask_app)
migrate = Migrate(flask_app, db)

db.init_app(flask_app)
with flask_app.app_context():
    db.create_all()

login_manager.init_app(flask_app)

from .auth import auth as auth_blueprint

flask_app.register_blueprint(auth_blueprint)

from .app import app as main_blueprint

flask_app.register_blueprint(main_blueprint)


# Instantiate the Flask class to the variable: app
def create_app():
    return flask_app
