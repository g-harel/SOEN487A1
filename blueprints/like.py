from flask import Blueprint, jsonify, request
import sqlalchemy

from db import db
from helpers import error_response, row_dictify
from models.like import Like

blueprint = Blueprint("like", __name__)
prefix = "/like"


@blueprint.route("/")
def get_all_like():
    like_list = Like.query.all()

    return jsonify([row_dictify(like) for like in like_list])


@blueprint.route("/<like_id>")
def get_like(like_id):
    like = Like.query.filter_by(id=like_id).first()

    if not like:
        return error_response(404, "Not Found")

    return jsonify(row_dictify(like))
