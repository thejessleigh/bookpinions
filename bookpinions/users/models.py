from utils import db


class User(db.Model):
    __tablename__ = 'users'

    goodreads_user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    created_time = db.Column(db.DateTime)
    visibility = db.Column(db.String(10), default="private")
    access_token = db.Column(db.String(255))
    access_secret = db.Column(db.String(255))

    def __init__(self, goodreads_user_id, name, created_time, username, access_token, access_secret):
        self.goodreads_user_id = goodreads_user_id
        self.created_time = created_time
        self.name = name
        self.username = username
        self.access_token = access_token
        self.access_secret = access_secret

    def __repr__(self):
        return "<Username: {username}>".format(
            name=self.name,
            username=self.username
        )
