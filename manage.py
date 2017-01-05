from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.database import db
from app import create_app
import app.bands.model
import app.comments.model
import app.songs.model
import app.versions.model
import app.votes.model


app = create_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()
