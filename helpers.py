from flask import jsonify, make_response


def error_response(code, msg):
    return make_response(jsonify({"code": code, "msg": msg}), code)


def row_dictify(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}
