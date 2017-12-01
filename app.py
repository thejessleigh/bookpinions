import os

from flask import Flask
import redis

from bookpinions import main_blueprint
from bookpinions.users import user_blueprint
from utils import db

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

# register blueprints
app.register_blueprint(main_blueprint, url_prefix='/')
app.register_blueprint(user_blueprint, url_prefix='/user')


if __name__ == '__main__':
    app.run()
