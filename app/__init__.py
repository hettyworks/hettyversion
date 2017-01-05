from flask import Flask
from app.database import db

class base_config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

def create_app(config=base_config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    return app
