from statappserver.src import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True)
    is_bot = db.Column(db.Boolean)
    fname = db.Column(db.String(128), nullable=True)
    lname = db.Column(db.String(128), nullable=True)
    username = db.Column(db.String(128), nullable=True)
    lang_code = db.Column(db.String(20))

    def __repr__(self):
        return f'<User: {self.telegram_id}, {self.username}>'

    def __str__(self):
        return self.__repr__()
