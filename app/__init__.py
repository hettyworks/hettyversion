from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.database import db
from app.versions.model import Version
from app.votes.model import Vote
from app.comments.model import Comment
from app.bands.model import Band
from app.songs.model import Song

class base_config(object):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/hettyversion'

def create_app(config=base_config):
    app = Flask(__name__)
    app.secret_key = 'some secret key'
    app.config.from_object(config)
    db.init_app(app)

    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(Version, db.session))
    admin.add_view(ModelView(Vote, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Band, db.session))
    admin.add_view(ModelView(Song, db.session))

    return app
