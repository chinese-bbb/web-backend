import os

from flask import Blueprint
from flask import render_template

bp = Blueprint('home', __name__, template_folder='../templates')

with open(os.path.join(os.path.dirname(__file__), '../version.txt')) as f:
    git_hash = f.readline()


@bp.route('/')
def home():
    return render_template('home.html', hash=git_hash)
