from flask import request, redirect, render_template, Blueprint, flash, session
from flask_app.decorators import login_required

pages = Blueprint('pages', __name__, template_folder='templates')


@pages.route('/github')
@login_required
def github():
    return render_template('github.html')
