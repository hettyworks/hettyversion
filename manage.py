from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.database import db
from app import create_app
import app.bands.model
import app.comments.model
from app.songs.model import Song
import app.versions.model
import app.votes.model
from app.data.scrape_songs import get_song_names

app = create_app()
app.app_context().push() # set default context
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())

@manager.command
def load_songdata():
    """
    Load songs from phish.net/songs into db
    """

    meta = db.metadata
    for table in meta.sorted_tables:
        if table.name == 'song':
            print('Clear table %s', table)
            db.session.execute(table.delete())
    db.session.commit()
    for name in get_song_names():
        s = Song()
        s.name = name
        s.band_id = 1
        db.session.add(s)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
