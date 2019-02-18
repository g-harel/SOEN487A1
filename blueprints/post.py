from flask import Blueprint, jsonify, request
import sqlalchemy

from db import db
from helpers import error_response, row_dictify
from models.post import Post

blueprint = Blueprint("post", __name__)
prefix = "/post"


@blueprint.route("/")
def get_all_post():
    post_list = Post.query.all()

    return jsonify([row_dictify(post) for post in post_list])


@blueprint.route("/<post_id>")
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return error_response(404, "Not Found")

    return jsonify(row_dictify(post))


@blueprint.route("/", methods={"PUT"})
def put_post():
    text = request.form.get("text")
    if not text:
        return make_response(403, "Missing Text")

    user_id = request.form.get("user_id")
    if not user_id:
        return make_response(403, "Missing User ID")

    post = Post(text=text, user_id=user_id)
    db.session.add(post)

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return error_response(500, "Cannot Write")

    return jsonify(row_dictify(post))
