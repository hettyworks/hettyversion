from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter

from hettyversion.database import db
import hettyversion.models
from hettyversion.config import base_config

from hettyversion.versions.views import version_blueprint
from hettyversion.shutdown import shutdown_blueprint
from hettyversion.users.views import user_blueprint


def create_app(config=base_config):
    app = Flask(__name__)
    app.secret_key = 'some secret key'
    app.config.from_object(config)
    app.register_blueprint(version_blueprint, url_prefix='/versions')
    app.register_blueprint(shutdown_blueprint)
    app.register_blueprint(user_blueprint)

    db.init_app(app)
    mail = Mail(app)

    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(hettyversion.models.Version, db.session))
    admin.add_view(ModelView(hettyversion.models.Vote, db.session))
    admin.add_view(ModelView(hettyversion.models.Comment, db.session))
    admin.add_view(ModelView(hettyversion.models.Band, db.session))
    admin.add_view(ModelView(hettyversion.models.Song, db.session))
    admin.add_view(ModelView(hettyversion.models.User, db.session))

    db_adapter = SQLAlchemyAdapter(db, hettyversion.models.User)
    user_manager = UserManager(db_adapter, app)

    return app
