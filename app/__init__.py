from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail

from app.database import db
from app.versions.model import Version
from app.votes.model import Vote
from app.comments.model import Comment
from app.bands.model import Band
from app.songs.model import Song
from app.users.model import User
from app.versions.views import version_blueprint
from app.shutdown import shutdown_blueprint
from app.users.views import user_blueprint

import os
from flask_user import UserManager, SQLAlchemyAdapter

class base_config(object):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    mysql_ip = os.getenv('HETTYVERSION_MYSQL_IP', '192.168.99.100');

    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@{0}/hettyversion'.format(mysql_ip);

    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"HettyVersion" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    print (MAIL_USERNAME, MAIL_PASSWORD)

    USER_APP_NAME        = "HettyVersion"

    DEBUG = True

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
    admin.add_view(ModelView(Version, db.session))
    admin.add_view(ModelView(Vote, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Band, db.session))
    admin.add_view(ModelView(Song, db.session))
    admin.add_view(ModelView(User, db.session))

    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app) 

    return app
