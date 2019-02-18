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
