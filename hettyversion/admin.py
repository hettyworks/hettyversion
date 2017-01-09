from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import hettyversion.models


class SongView(ModelView):
    column_list = (
        hettyversion.models.Song.song_id,
        hettyversion.models.Song.name,
        hettyversion.models.Song.desc,
        hettyversion.models.Song.band_id
    )
    can_delete = False


def create_admin(app, db, name='microblog', template_mode='bootstrap3'):
    admin = Admin(app, name=name, template_mode=template_mode)

    admin.add_view(ModelView(hettyversion.models.Version, db.session))
    admin.add_view(ModelView(hettyversion.models.Vote, db.session))
    admin.add_view(ModelView(hettyversion.models.Comment, db.session))
    admin.add_view(ModelView(hettyversion.models.Band, db.session))
    admin.add_view(SongView(hettyversion.models.Song, db.session))
    admin.add_view(ModelView(hettyversion.models.User, db.session))

    return admin