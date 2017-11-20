import json
import os

from flask import Flask
from goodreads.client import GoodreadsClient

app = Flask(__name__)

gc = GoodreadsClient(os.environ['GOODREADS_KEY'], os.environ['GOODREADS_SECRET'])


@app.route("/")
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
