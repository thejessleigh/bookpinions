from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    goodreads_user_id = db.Column(db.Integer, nullable=False)
    name = db.Colmn(db.String(255))
    created_time = db.Column(db.DateTime)
    visibility = db.Column(db.String(10), default="private")

    def __init__(self, goodreads_user_id, name, created_time):
        self.goodreads_user_id = goodreads_user_id
        self.created_time = created_time
        self.name = name

    def __repr__(self):
        return "<User id: {id}, Name: {name}>".format(
            id=self.id,
            name=self.name
        )
