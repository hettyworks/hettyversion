from flask import redirect, Blueprint, render_template, session, request, flash, abort, Markup
from flask_user import login_required, current_user
from hettyversion.models import Vote, Band, Song, Version, VersionComment, User, Venue, Show, ListenedTo
from hettyversion.database import db
from hettyversion.forms import VersionForm, VoteForm, VersionCommentForm
from hettyversion.versions import get_candidate, fight_versions
from datetime import datetime
from hettyversion.data import \
    get_version_by_id, get_song_by_id, get_song_by_phishin_id, get_band_id, mark_listenedto
from sqlalchemy import func, or_, and_

frontend = Blueprint('frontend', __name__)

@frontend.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')

def add_vote(lhs_id, rhs_id, winner):
    v = Vote(lhs=lhs_id, rhs=rhs_id, winner=winner, created_by=current_user.id, created=datetime.utcnow())
    db.session.add(v)
    db.session.commit()

def update_rating(lhs_id, rhs_id, winner):
    fight_versions(lhs_id, rhs_id, winner)
    add_vote(lhs_id, rhs_id, winner)

def get_random_phish_song(exclude=None):
    song_id = db.session.query(Song.phishin_id) \
                     .join(Band, Band.band_id == Song.band_id) \
                     .filter(Band.name == 'Phish')

    if exclude is not None:
        song_id = song_id.filter(Song.phishin_id != exclude)

    song_id = song_id.order_by(func.rand()).first().phishin_id
    return song_id

@frontend.route('/vote/', methods=['GET', 'POST'])
@login_required
def present_vote():
    form = VoteForm()
    if form.validate_on_submit():
        lhs_id = int(form.lhs_id.data)
        rhs_id = int(form.rhs_id.data)
        (winner_id, loser_id) = (lhs_id, rhs_id) if form.lhs.data else (rhs_id, lhs_id)
        update_rating(lhs_id, rhs_id, winner_id)
        winner = get_version_by_id(winner_id)
        loser = get_version_by_id(loser_id)
        song = get_song_by_phishin_id(winner.song_id)
        flash(Markup('You voted for <a href="/versions/{}">{}</a> over <a href="/versions/{}">{}</a>.  Leave your review on the individual version pages.'.format(winner_id, winner.date, loser_id, loser.date)))
        return redirect('/vote?song_id={}'.format(winner.song_id))
    else:
        song_id = request.args.get('song_id')
        lhs, rhs = None, None
        while lhs == None and rhs == None:
            if song_id is None:
                song_id = get_random_phish_song()
            lhs, rhs = get_candidate(song_id)
            if lhs == None or rhs == None:
                song_id = None
        form.init_candidate(lhs, rhs)
        print(lhs)
        return render_template('vote.html', form=form, lhs=lhs, rhs=rhs)


# False is 0 true is 1
@frontend.route('/listenedto', methods=['POST'])
def listenedto():
    version_id = request.json['version_id']
    listened_to = request.json['listened_to']
    if current_user.is_authenticated:
        return mark_listenedto(current_user.get_id(),version_id,listened_to)
    else:
        abort(403)


@frontend.route('/bands/')
def bands_page():
    bands = db.session.query(Band.name,Band.band_id,func.count(Song.song_id).label('count')).outerjoin(Song, \
        Band.band_id == Song.band_id).group_by(Band.band_id).all()
    return render_template('band_list.html', bands=bands)


@frontend.route('/bands/<band_id>')
def single_band(band_id):
    band = db.session.query(Band).filter(Band.band_id==band_id).one()
    songs = db.session.query(Song.song_id,Song.name,func.count(Version.song_id).label('count')) \
        .outerjoin(Version, Song.phishin_id == Version.song_id) \
        .group_by(Song.song_id).filter(Song.band_id==band_id).all()
    return render_template('single_band.html', band=band, songs=songs)


@frontend.route('/phish')
def single_phish():
    band_id = get_band_id('Phish')
    band = db.session.query(Band).filter(Band.band_id==band_id).one()
    songs = db.session.query(Song.song_id,Song.name,func.count(Version.song_id).label('count')) \
        .outerjoin(Version, Song.phishin_id == Version.song_id) \
        .group_by(Song.song_id).filter(Song.band_id==band_id).all()
    return render_template('single_band.html', band=band, songs=songs)


@frontend.route('/songs/<song_id>')
def single_song(song_id):
    song = db.session.query(Song).filter(Song.song_id==song_id).one()

    versions = db.session.query(Version.date,Version.version_id,Version.mu,func.count(Vote.vote_id).label('count'), \
        func.count(ListenedTo.lt_id).label('lt_id')) \
        .outerjoin(ListenedTo, and_(ListenedTo.version_id == Version.version_id, ListenedTo.user_id == current_user.get_id())) \
        .outerjoin(Vote, or_(Vote.lhs == Version.version_id, Vote.rhs == Version.version_id)) \
        .filter(Version.song_id==song.phishin_id) \
        .group_by(Version.version_id).subquery('versions')

    versions_with_comments = db.session.query(versions, func.count(VersionComment.versioncomment_id).label('vc_count')) \
        .outerjoin(VersionComment, VersionComment.version_id == versions.c.version_id) \
        .group_by(versions.c.version_id) \
        .order_by(versions.c.mu.desc(),versions.c.count.desc(),func.count(VersionComment.versioncomment_id).desc())

    versions = versions_with_comments.all()

    return render_template('single_song.html', song=song, versions=versions)


@frontend.route('/vote')
def random_vote():
    exclude = request.args.get('exclude')
    new_id = get_random_phish_song(exclude=exclude)
    if new_id is None:
        return redirect('/')
    return redirect('/vote/?song_id={}'.format(new_id))


@frontend.route('/versions/<version_id>')
def single_version(version_id):
    version = db.session.query(Version.date,Version.url,ListenedTo.lt_id.label('lt_id'),Version.mu,Version.version_id,Song.name.label('song_name'),Song.song_id,Show.show_id,Venue.name.label('venue_name'),Venue.location) \
        .outerjoin(ListenedTo, and_(ListenedTo.user_id == current_user.get_id(), ListenedTo.version_id == version_id)) \
        .join(Song, Song.phishin_id == Version.song_id) \
        .join(Show, Show.phishin_id == Version.show_id) \
        .join(Venue, Show.venue_id == Venue.phishin_id) \
        .filter(Version.version_id==version_id).one()
    comments = db.session.query(VersionComment.body,User.username.label('author')).outerjoin(User, User.id == VersionComment.author_id) \
        .filter(VersionComment.version_id==version_id).order_by(VersionComment.comment_date.desc()).all()
    return render_template('single_version.html', version=version, comments=comments)


@frontend.route('/versions/<version_id>/comment', methods=['GET', 'POST'])
@login_required
def new_versioncomment(version_id):
    form = VersionCommentForm()
    if form.validate_on_submit():
        vc = VersionComment(version_id=version_id,author_id=current_user.id,body=form.body.data,comment_date=datetime.utcnow())
        db.session.add(vc)
        db.session.commit()
        flash('You left a comment.')
        version = get_version_by_id(version_id)
        return redirect('/versions/' + version_id)
    else:
        version = get_version_by_id(version_id)
        song = get_song_by_id(version.song_id)
        return render_template('version_comment.html',form=form,version=version,song=song,user=current_user)


@frontend.route('/members/', methods=['GET'])
@login_required
def members_page():
    return render_template('members.html')
