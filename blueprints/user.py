from flask import Blueprint, jsonify, request
import sqlalchemy

from db import db
from helpers import error_response, row_dictify
from models.user import User

blueprint = Blueprint("user", __name__)
prefix = "/user"


@blueprint.route("/")
def get_all_user():
    user_list = User.query.all()

    return jsonify([row_dictify(user) for user in user_list])


@blueprint.route("/<user_id>")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return error_response(404, "Not Found")

    return jsonify(row_dictify(user))


@blueprint.route("/<user_id>/posts")
def get_user_posts(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return error_response(404, "Not Found")

    return jsonify([row_dictify(post) for post in user.posts])


@blueprint.route("/<user_id>/likes")
def get_user_likes(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return error_response(404, "Not Found")

    return jsonify([row_dictify(like) for like in user.likes])


@blueprint.route("/", methods={"PUT"})
def put_user():
    name = request.form.get("name")
    if not name:
        return error_response(403, "Missing 'name'")

    user = User(name=name)
    db.session.add(user)

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return error_response(500, "Cannot Write")

    return jsonify(row_dictify(user))
