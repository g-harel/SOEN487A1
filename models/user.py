from db import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False, unique=True)

    posts = db.relationship("Post", back_populates="user")
    likes = db.relationship("Like", back_populates="user")
