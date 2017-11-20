import json
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from goodreads.client import GoodreadsClient

app = Flask(__name__)

# Set up database
db = SQLAlchemy()
db.app = app
db.init_app(app)

# Set up goodreads client
gc = GoodreadsClient(os.environ['GOODREADS_KEY'], os.environ['GOODREADS_SECRET'])

# Check app and goodreads client status
@app.route("/status")
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


