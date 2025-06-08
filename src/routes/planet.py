from flask import jsonify, Blueprint, request
from models.Planet import Planet
from database.db import db

api = Blueprint('api/planet', __name__)

@api.route('/', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    all_planets = [planet.serialize() for planet in planets]
    return jsonify({"planets": all_planets}), 200

@api.route('/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planet.query.filter_by(id=id).first()
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@api.route('/create', methods=['POST'])
def create_planet():
    body = request.get_json()

    exist = Planet.query.filter_by(name=body["name"]).first()
    if exist:
        return jsonify({"msg": "Planet already exist"}), 404

    new_planet = Planet(
        name=body["name"],
        population=body.get("population", 0),
        terrain=body.get("terrain", "unknown"),
        climate=body.get("climate", "unknown")
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 200