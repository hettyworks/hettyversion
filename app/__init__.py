from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.database import db
from app.versions.model import Version
from app.votes.model import Vote
from app.comments.model import Comment
from app.bands.model import Band
from app.songs.model import Song
from app.versions.views import version

import os

class base_config(object):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    mysql_ip = os.getenv('HETTYVERSION_MYSQL_IP', '192.168.99.100');
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@{0}/hettyversion'.format(mysql_ip);

def create_app(config=base_config):
    app = Flask(__name__)
    app.secret_key = 'some secret key'
    app.config.from_object(config)
    app.register_blueprint(version, url_prefix='/versions')

    db.init_app(app)

    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(Version, db.session))
    admin.add_view(ModelView(Vote, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Band, db.session))
    admin.add_view(ModelView(Song, db.session))

    return app
