from flask import jsonify
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app import app
from db import db
from blueprints import like, post, user
from helpers import status_response


@app.errorhandler(404)
def page_not_found(e):
    return status_response(404, "Not Found")


@app.route('/')
def SOEN487A1():
    return jsonify({
        "title": "SOEN487 Assignment 1",
        "student": {
            "id": "40006459",
            "name": "Gabriel Harel"
        }
    })

app.register_blueprint(like.blueprint, url_prefix=like.prefix)
app.register_blueprint(post.blueprint, url_prefix=post.prefix)
app.register_blueprint(user.blueprint, url_prefix=user.prefix)


# By default, foreign key constraints are not enforced in sqlite.
# https://stackoverflow.com/a/12770354/3053361
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run()
