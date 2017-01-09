from flask import redirect, Blueprint, render_template
from flask_user import login_required, current_user
from hettyversion.models import Vote
from hettyversion.database import db
from hettyversion.forms import VersionForm, VoteForm
from hettyversion.versions import get_candidate, fight_versions
from datetime import datetime

frontend = Blueprint('frontend', __name__)

@frontend.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')

@frontend.route('/versions/', methods=['GET', 'POST'])
def create_version():
    form = VersionForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('new_version.html', form=form)

def add_vote(lhs_id, rhs_id, winner):
    v = Vote(lhs=lhs_id, rhs=rhs_id, winner=winner, created_by=current_user.id, created=datetime.now())
    db.session.add(v)
    db.session.commit()

def update_rating(lhs_id, rhs_id, winner):
    fight_versions(lhs_id, rhs_id, winner)
    add_vote(lhs_id, rhs_id, winner)

@frontend.route('/vote/', methods=['GET', 'POST'])
def present_vote():
    form = VoteForm()
    if form.validate_on_submit():
        lhs_id = int(form.lhs_id.data)
        rhs_id = int(form.rhs_id.data)
        if form.lhs.data:
            update_rating(lhs_id, rhs_id, lhs_id)
            return redirect('/lhs-wins')
        elif form.rhs.data:
            update_rating(lhs_id, rhs_id, rhs_id)
            return redirect('/rhs-wins')
    else:
        lhs, rhs = get_candidate()
        form.init_candidate(lhs, rhs)
        return render_template('vote.html', form=form)

@frontend.route('/members/', methods=['GET'])
@login_required
def members_page():
    return render_template('members.html')
