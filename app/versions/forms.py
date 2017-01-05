from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField

class VersionForm(FlaskForm):
    name = StringField('title')
    date = DateField('date')
    song_id = IntegerField('song_id')
    url = StringField('url')
