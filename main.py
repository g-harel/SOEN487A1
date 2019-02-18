from flask import jsonify

from app import app
from db import db
from blueprints import like, post, user
from helpers import error_response


@app.errorhandler(404)
def page_not_found(e):
    return error_response(404, "Not Found")


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

if __name__ == '__main__':
    db.create_all()
    app.run()
