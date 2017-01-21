from flask_wtf import FlaskForm, Form
from wtforms import StringField, DateField, IntegerField, SubmitField, HiddenField, Label, TextAreaField, validators

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
        self.lhs.label = Label(None, lhs.date)
        self.rhs.label  = Label(None, rhs.date)
        self.lhs_id.data = lhs.version_id
        self.rhs_id.data = rhs.version_id


class VersionCommentForm(FlaskForm):
    body = TextAreaField(u'Comment Text', [validators.required(), validators.length(max=4096)])
