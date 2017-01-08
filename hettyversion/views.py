from flask import redirect, Blueprint, render_template
from flask_user import login_required

from hettyversion.forms import VersionForm

frontend = Blueprint('frontend', __name__)

@frontend.route('/versions/', methods=['GET', 'POST'])
def create_version():
    form = VersionForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('new_version.html', form=form)


@frontend.route('/members/', methods=['GET'])
@login_required
def members_page():
	return render_template('members.html')