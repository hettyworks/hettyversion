from flask import (
    current_app, request, redirect, url_for, render_template, flash, abort,
)
from hettyversion.models import Version
from hettyversion.versions.forms import VersionForm
from flask import Blueprint

version_blueprint = Blueprint('version_blueprint', __name__)

@version_blueprint.route('/', methods=['GET', 'POST'])
def create_version():
    form = VersionForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('new_version.html', form=form)
