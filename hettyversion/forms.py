from flask_wtf import FlaskForm, Form
from wtforms import StringField, DateField, IntegerField, SubmitField, HiddenField, Label

class VersionForm(FlaskForm):
    name = StringField('title')
    date = DateField('date')
    song_id = IntegerField('song_id')
    url = StringField('url')


class VoteForm(Form):
    lhs = SubmitField()
    rhs = SubmitField()
    lhs_id = HiddenField()
    rhs_id = HiddenField()

    def init_candidate(self, lhs, rhs):
        self.lhs.label = Label(None, lhs.title)
        self.rhs.label  = Label(None, lhs.title)
        self.lhs_id.data = lhs.version_id
        self.rhs_id.data = rhs.version_id
