import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

basedir = os.path.abspath(os.path.dirname(__file__))

# Instantiate the Flask class to the variable: app
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'SECRET_KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    bootstrap = Bootstrap(app)
    moment = Moment(app)
    migrate = Migrate(app, db)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .app import app as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
