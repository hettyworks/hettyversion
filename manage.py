from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from hettyversion.database import db
from hettyversion import create_app
from hettyversion.models import Song, Version, Band
from hettyversion.data.scrape_songs import get_song_names
from hettyversion.data.dev import get_song_id, get_song_versions, get_band_id

app = create_app()
app.app_context().push() # set default context
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


@manager.command
def load_demo():
    load_bands()
    load_songdata(band_id=get_band_id(db, 'Phish'))
    load_hoodvers()


@manager.command
def load_songdata(band_id=1):
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
        s.band_id = band_id
        db.session.add(s)
    db.session.commit()


@manager.command
def load_bands():
    meta = db.metadata
    for table in meta.sorted_tables:
        if table.name == 'band':
            print('Clear table %s', table)
            db.session.execute(table.delete())
    db.session.commit()
    b = Band()
    b.name = 'Phish'
    db.session.add(b)
    db.session.commit()
    b = Band()
    b.name = 'Sting'
    db.session.add(b)
    db.session.commit()
    b = Band()
    b.name = 'Katy Perry'
    db.session.add(b)
    db.session.commit()


@manager.command
def load_hoodvers():
    # Get Harry Hood song_id
    
    meta = db.metadata
    for table in meta.sorted_tables:
        if table.name == 'version':
            print('Clearing table: version.')
            db.session.execute(table.delete())
    db.session.commit()

    song_id = get_song_id(db, 'Harry Hood')
    for version in get_song_versions('Harry Hood'):
        v = Version()
        v.title = version
        v.song_id = song_id
        db.session.add(v)
    db.session.commit()

if __name__ == '__main__':
    manager.run()