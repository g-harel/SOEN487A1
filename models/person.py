from db import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<Person {}: {}>".format(self.id, self.name)
