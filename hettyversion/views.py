from flask import redirect, Blueprint, render_template
from flask_user import login_required
from hettyversion.forms import VersionForm, VoteForm
from hettyversion.versions import get_candidate, fight_versions

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

@frontend.route('/vote/', methods=['GET', 'POST'])
def present_vote():
    form = VoteForm()
    if form.validate_on_submit():
        if form.lhs.data:
            return redirect('/lhs-wins')
        elif form.rhs.data:
            return redirect('/rhs-wins')
    else:
        lhs, rhs = get_candidate()
        form.init_candidate(lhs, rhs)
        return render_template('vote.html', form=form)

@frontend.route('/members/', methods=['GET'])
@login_required
def members_page():
    return render_template('members.html')
