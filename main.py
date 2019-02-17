from app import app
from db import db
from blueprints import person
from helpers import error_response

app.register_blueprint(person.blueprint, url_prefix=person.prefix)


@app.errorhandler(404)
def page_not_found(e):
    return error_response(404, "Not Found")


@app.route('/')
def SOEN487A1():
    return """{
        "title": "SOEN487 Assignment 1",
        "student": {
            "id": "40006459",
            "name": "Gabriel Harel"
        }
    }"""

if __name__ == '__main__':
    db.create_all()
    app.run()
