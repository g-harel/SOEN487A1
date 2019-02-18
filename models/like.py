from db import db


class Like(db.Model):
    __tablename__ = "like"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    user = db.relationship('User', back_populates="likes")
    post = db.relationship('Post', back_populates="likes")
