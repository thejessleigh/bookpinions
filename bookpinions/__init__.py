import json

from flask import Blueprint

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
