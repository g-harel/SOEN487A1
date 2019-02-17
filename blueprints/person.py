from flask import Blueprint, jsonify, request
import sqlalchemy

from db import db
from helpers import error_response, row_dictify
from models.person import Person

blueprint = Blueprint("person", __name__)
prefix = "/person"


@blueprint.route("/")
def get_all_person():
    person_list = Person.query.all()

    return jsonify([row_dictify(person) for person in person_list])


@blueprint.route("/<person_id>")
def get_person(person_id):
    person = Person.query.filter_by(id=person_id).first()

    if not person:
        return error_response(404, "Person Not Found")

    return jsonify(row_dictify(person))


@blueprint.route("/", methods={"PUT"})
def put_person():
    name = request.form.get("name")

    if not name:
        return make_response(403, "Missing Name")

    person = Person(name=name)
    db.session.add(person)

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return error_response(404, "Cannot Write")

    return jsonify(row_dictify(person))
