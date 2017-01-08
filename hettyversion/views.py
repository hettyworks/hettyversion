from flask import redirect, Blueprint, render_template, render_template_string
from flask_user import login_required

from hettyversion.versions.forms import VersionForm

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
	return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
            {% endblock %}
            """) 