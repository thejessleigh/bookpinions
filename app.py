import json
import os

from flask import Flask
from goodreads.client import GoodreadsClient
import redis

from bookpinions.users import user_blueprint
from database import db

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up database
db.app = app
db.init_app(app)
redis_db = redis.StrictRedis(
    host=app.config.get('REDIS_HOST'),
    port=app.config.get('REDIS_PORT'),
    decode_responses=True
)

# Set up goodreads client
gc = GoodreadsClient(os.environ['GOODREADS_KEY'], os.environ['GOODREADS_SECRET'])

app.register_blueprint(user_blueprint, url_prefix='/user')

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

if __name__ == '__main__':
    app.run()
