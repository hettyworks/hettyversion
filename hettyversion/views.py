from flask import redirect, Blueprint, render_template, session, request
from flask_user import login_required, current_user
from hettyversion.models import Vote, Band, Song, Version
from hettyversion.database import db
from hettyversion.forms import VersionForm, VoteForm
from hettyversion.versions import get_candidate, fight_versions
from datetime import datetime
from hettyversion.data.dev import get_version_by_id, get_song_by_id
from sqlalchemy import func, or_

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
        song_id = request.args.get('song_id')
        if song_id is None:
            raise Exception("song_id not provided in query string.")
        print('song_id: ' + song_id)
        lhs, rhs = get_candidate(song_id)
        form.init_candidate(lhs, rhs)
        return render_template('vote.html', form=form)

@frontend.route('/bands/')
def bands_page():
    bands = db.session.query(Band.name,Band.band_id,func.count(Song.song_id).label('count')).outerjoin(Song, Band.band_id == Song.band_id).group_by(Band.band_id).all()
    return render_template('band_list.html', bands=bands)


@frontend.route('/bands/<band_id>')
def single_band(band_id):
    band = db.session.query(Band).filter(Band.band_id==band_id).one()
    songs = db.session.query(Song.song_id,Song.name,func.count(Version.song_id).label('count')).outerjoin(Version, Song.song_id == Version.song_id).group_by(Song.song_id).filter(Song.band_id==band_id).all()
    return render_template('single_band.html', band=band, songs=songs)


@frontend.route('/songs/<song_id>')
def single_song(song_id):
    song = db.session.query(Song).filter(Song.song_id==song_id).one()
    versions = db.session.query(Version.title,Version.mu,func.count(Vote.vote_id).label('count')).outerjoin(Vote, or_(Vote.lhs == Version.version_id, Vote.rhs == Version.version_id)).filter(Version.song_id==song_id).group_by(Version.version_id).order_by(Version.mu.desc()).all()
    return render_template('single_song.html', song=song, versions=versions)


@frontend.route('/versions/<version_id>')
def single_version(version_id):
    version = db.session.query(Version.title,Version.mu,Song.name.label('song_name'),Song.song_id).outerjoin(Song, Song.song_id == Version.song_id).filter(Version.version_id==version_id).one()
    return render_template('single_version.html', version=version)


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
