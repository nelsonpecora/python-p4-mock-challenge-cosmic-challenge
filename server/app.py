#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# initialize the restful api
api = Api(app)


# gets all scientists from API
class ScientistList(Resource):
    def get(self):
        scientists = Scientist.query.all()
        return [scientist.to_dict(rules=("-missions",)) for scientist in scientists]


api.add_resource(ScientistList, '/scientists')

# gets individual scientist by ID with list of missions


class ScientistItem(Resource):
    def get(self, id):
        scientist = Scientist.query.get(id)
        if scientist:
            return scientist.to_dict()
        else:
            return {"error": "Scientist not found"}, 404


api.add_resource(ScientistItem, '/scientists/<int:id>')


# POST scientist

# @app.route('/')
# def home():
#     return ''


if __name__ == '__main__':
    app.run(port=5555, debug=True)
