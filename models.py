from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(150))

    phone = db.Column(db.String(20))

    address = db.Column(db.String(200))

    spouse = db.Column(db.String(150))

    next_of_kin = db.Column(db.String(150))

    bank_account = db.Column(db.String(150))

    place_of_retirement = db.Column(db.String(200))

    registration_id = db.Column(db.String(20), unique=True)

    status = db.Column(db.String(20), default="Pending")

    def __repr__(self):
        return f"<User {self.username}>"