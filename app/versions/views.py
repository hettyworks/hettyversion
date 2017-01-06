from flask import (
    current_app, request, redirect, url_for, render_template, flash, abort,
)
from app.versions.model import Version
from app.versions.forms import VersionForm
from flask import Blueprint

version = Blueprint('vers', __name__)

@version.route('/', methods=['GET', 'POST'])
def create_version():
    form = VersionForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('new_version.html', form=form)
