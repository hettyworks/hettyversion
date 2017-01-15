from flask import Flask
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask_sslify import SSLify

from hettyversion.database import db
from hettyversion.config import base_config
from hettyversion.admin import create_admin
from hettyversion.views import frontend
from hettyversion.models import User


def create_app(config=base_config):
    app = Flask(__name__, static_path='/hettyversion/static')
    app.secret_key = 'some secret key'
    app.config.from_object(config)
    app.register_blueprint(frontend)

    db.init_app(app)
    mail = Mail(app)

    admin = create_admin(app, db)

    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)

    #sslify = SSLify(app, skips=[''])

    return app
