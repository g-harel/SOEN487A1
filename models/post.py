from db import db


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.Text(), nullable=False)

    user = db.relationship("User", back_populates="posts")
    likes = db.relationship("Like", back_populates="post")
