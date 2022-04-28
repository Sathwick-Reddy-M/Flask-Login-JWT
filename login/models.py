from login.db import db


class User(db.Model):
    __tablename__ = 'passengers'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), nullable=False, unique=True)
    user_pwd = db.Column(db.String(80), nullable=False)

    def __init__(self, user_name, user_pwd):
        self.user_name = user_name
        self.user_pwd = user_pwd

    def __repr__(self):
        return f'{self.user_id}, {self.user_name}'
