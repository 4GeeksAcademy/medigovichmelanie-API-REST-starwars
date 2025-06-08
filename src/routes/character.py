from flask import jsonify, Blueprint, request
from models.Character import Character
from database.db import db

api = Blueprint('api/character', __name__)


@api.route('/', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    all_characters = [char.serialize() for char in characters]
    return jsonify({"characters": all_characters}), 200

@api.route('/<int:id>', methods=['GET'])
def get_character_by_id(id):
    character = Character.query.filter_by(id=id).first()
    return jsonify(character.serialize()), 200


@api.route('/create', methods=['POST'])
def create_character():
    body = request.get_json()

    exist = Character.query.filter_by(name=body["name"]).first()
    if exist:
        return jsonify({"msg": "Character already exist"}), 404

    new_character = Character(name=body["name"], gender=body["gender"],
                              hair_color=body["hair_color"], eye_color=body["eye_color"])

    db.session.add(new_character)
    db.session.commit()

    return jsonify(new_character.serialize()), 200