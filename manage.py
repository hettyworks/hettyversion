from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from hettyversion.database import db
from hettyversion import create_app
from hettyversion.models import Song, User, Version, Band, Role
from hettyversion.data.scrape_songs import get_song_names
from hettyversion.data.dev import get_song_id, get_song_versions, get_band_id
from pprint import pprint

app = create_app()
app.app_context().push() # set default context so db.session can find the app
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


@manager.command
def list_roles():
    pprint([vars(r) for r in db.session.query(Role).all()])

@manager.command
def add_role(role_name):
    r = Role()
    r.name = role_name
    db.session.add(r)
    db.session.commit()

def dissoc(d, key):
    d.pop(key, None)
    return d

def print_model(m):
    data = vars(m).copy()
    pprint(dissoc(data, "_sa_instance_state"))

@manager.command
def list_users(limit=5):
    for user in db.session.query(User).all():
        print_model(user)
        for role in user.roles:
            print("Roles")
            print_model(role)

@manager.command
def grant_role(user_id, role_id):
    role = db.session.query(Role).filter(Role.id==int(role_id)).one()
    user = db.session.query(User).filter(User.id==int(user_id)).one()
    user.roles.append(role)
    db.session.commit()

@manager.command
def load_demo():
    clear_data()
    load_bands()
    load_songdata(band_id=get_band_id(db, 'Phish'))
    load_yemvers()
    #load_vers()


def clear_data():
    meta = db.metadata
    for table in meta.sorted_tables:
        if table.name == 'version':
            print('Clear table %s', table)
            db.session.execute(table.delete())
    for table in meta.sorted_tables:
        if table.name == 'song':
            print('Clear table %s', table)
            db.session.execute(table.delete())
    for table in meta.sorted_tables:
        if table.name == 'band':
            print('Clear table %s', table)
            db.session.execute(table.delete())
    db.session.commit()

def load_songdata(band_id=1):
    """
    Load songs from phish.net/songs into db
    """
    for name in get_song_names():
        s = Song()
        s.name = name
        s.band_id = band_id
        db.session.add(s)
    db.session.commit()


def load_bands():
    b = Band()
    b.name = 'Phish'
    db.session.add(b)
    b = Band()
    b.name = 'Sting'
    db.session.add(b)
    b = Band()
    b.name = 'Katy Perry'
    db.session.add(b)
    db.session.commit()


def load_hoodvers():
    # Get Harry Hood song_id
    song_id = get_song_id(db, 'Harry Hood')
    for version in get_song_versions('Harry Hood'):
        v = Version()
        v.title = version
        v.song_id = song_id
        db.session.add(v)
    db.session.commit()

def load_yemvers():
    # test for get yem song_id
    song_id = get_song_id(db, 'You Enjoy Myself')
    for version in get_song_versions('You Enjoy Myself'):
        v = Version()
        v.title = version
        v.song_id = song_id
        db.session.add(v)
    db.session.commit() 
            

if __name__ == '__main__':
    manager.run()
