from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from config import config
from flask_login import LoginManager
from flask_assets import Environment, Bundle


mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__, static_url_path='')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    assets = Environment(app)
    assets.url = app.static_url_path
    assets.debug = True
    scss = Bundle('scss/_variables.scss',
    filters='pyscss',
    output='gen/ripper.min.css')
    assets.register('scss_all', scss)


    from .main import main as main_blueprint
    from .admin import admin as admin_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(auth_blueprint)

    return app