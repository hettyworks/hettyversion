from flask import Blueprint, render_template_string
from flask_user import login_required

user_blueprint = Blueprint('users_blueprint', __name__)

@user_blueprint.route('/members')
@login_required
def members_page():
	return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
            {% endblock %}
            """) 