from flask import redirect, Blueprint, render_template, session
from flask_user import login_required, current_user
from hettyversion.models import Vote, Version
from hettyversion.database import db
from hettyversion.forms import VersionForm, VoteForm
from hettyversion.versions import get_candidate, fight_versions
from datetime import datetime
from hettyversion.data.dev import get_version_by_id, get_song_by_id

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
@login_required
def present_vote():
    form = VoteForm()
    if form.validate_on_submit():
        lhs_id = int(form.lhs_id.data)
        rhs_id = int(form.rhs_id.data)
        (winner_id, loser_id) = (lhs_id, rhs_id) if form.lhs.data else (rhs_id, lhs_id)
        update_rating(lhs_id, rhs_id, winner_id)
        session['winner_id'] = winner_id
        session['loser_id'] = loser_id
        return redirect('/vote-result')
    else:
        lhs, rhs = get_candidate()
        form.init_candidate(lhs, rhs)
        return render_template('vote.html', form=form)

@frontend.route('/vote-result/')
@login_required
def vote_result():
    try:
        winner_id = session['winner_id']
        loser_id = session['loser_id']

        session.pop('winner_id')
        session.pop('loser_id')
    except KeyError:
        return redirect('/vote')

    winner = get_version_by_id(db, winner_id)
    loser = get_version_by_id(db, loser_id)
    song = get_song_by_id(db, winner.song_id)

    return render_template('vote_result.html', winner=winner, loser=loser, song=song)

@frontend.route('/members/', methods=['GET'])
@login_required
def members_page():
    return render_template('members.html')
