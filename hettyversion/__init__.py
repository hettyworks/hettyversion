from flask import Flask, request, redirect
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter

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

    @app.before_request
    def before_request():
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

    return app
