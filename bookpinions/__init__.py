import json

from flask import Blueprint, render_template

from bookpinions.templates import template_env
from utils import gc

main_blueprint = Blueprint('main', __name__)

# Check app and goodreads client status
@main_blueprint.route("status")
def status():
    book = gc.book(1)
    status_dict = {
        'app_status': True,
        'goodreads_api_call_status': {
            'book': book.title,
            'author': [author.name for author in book.authors]
        }
    }
    return json.dumps(status_dict)

@main_blueprint.route("/")
def home():
    return render_template(template_env.get_template('home.html'))
