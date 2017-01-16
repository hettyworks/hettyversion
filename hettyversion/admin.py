from flask import redirect, url_for, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_user import current_user

import hettyversion.models


class AuthModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_roles(['admin'])

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class SongView(AuthModelView):
    column_list = (
        hettyversion.models.Song.song_id,
        hettyversion.models.Song.name,
        hettyversion.models.Song.desc,
        hettyversion.models.Song.band_id
    )
    can_delete = False



def create_admin(app, db, name='microblog', template_mode='bootstrap3'):
    admin = Admin(app, name=name, template_mode=template_mode)

    admin.add_view(AuthModelView(hettyversion.models.Version, db.session))
    admin.add_view(AuthModelView(hettyversion.models.Vote, db.session))
    admin.add_view(AuthModelView(hettyversion.models.Comment, db.session))
    admin.add_view(AuthModelView(hettyversion.models.Band, db.session))
    admin.add_view(SongView(hettyversion.models.Song, db.session))
    admin.add_view(AuthModelView(hettyversion.models.User, db.session))
    admin.add_view(AuthModelView(hettyversion.models.VersionComment, db.session))

    return admin
