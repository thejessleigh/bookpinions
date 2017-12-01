import os

from flask.ext.sqlalchemy import SQLAlchemy
from goodreads.client import GoodreadsClient

db = SQLAlchemy()

gc = GoodreadsClient(os.environ['GOODREADS_KEY'], os.environ['GOODREADS_SECRET'])
