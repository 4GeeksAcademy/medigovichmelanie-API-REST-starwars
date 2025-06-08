from flask import jsonify, Blueprint, request
from models.User import User
from models.Favorite import Favorite
from models.Character import Character
from models.Planet import Planet
from database.db import db

api = Blueprint('api/user', __name__)

@api.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users = [user.serialize() for user in users]
    return jsonify(all_users), 200

@api.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": f"user not found {user_id}"}), 404
    return jsonify(user.serialize()), 200

@api.route('/register', methods=['POST'])
def create_users():
    body = request.get_json()

    exist = User.query.filter_by(email=body["email"]).first()
    if exist:
        return jsonify({"msg": "User already exist"}), 404

    new_user = User(
        username=body["username"], 
        email=body["email"],
        password=body["password"], 
        is_active=True,
        firstname=body.get("firstname", ""),
        lastname=body.get("lastname", "")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200

@api.route('/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    favorites_list = []
    for fav in favorites:
        favorite_data = {"id": fav.id}
        if fav.character_id:
            character = Character.query.get(fav.character_id)
            favorite_data["type"] = "character"
            favorite_data["data"] = character.serialize()
        elif fav.planet_id:
            planet = Planet.query.get(fav.planet_id)
            favorite_data["type"] = "planet"
            favorite_data["data"] = planet.serialize()
        favorites_list.append(favorite_data)
    
    return jsonify(favorites_list), 200

@api.route('/<int:user_id>/favorite/character/<int:character_id>', methods=['POST'])
def add_character_favorite(user_id, character_id):
    exist = Favorite.query.filter_by(
        user_id=user_id, character_id=character_id).first()
    if exist:
        return jsonify({"msg": "Favorite already exist"}), 404
    
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msg": "Character not found"}), 404
        
    new_favorite = Favorite(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite added"}), 201

@api.route('/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(user_id, planet_id):
    exist = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if exist:
        return jsonify({"msg": "Favorite already exist"}), 404
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
        
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite added"}), 201

@api.route('/<int:user_id>/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_character_favorite(user_id, character_id):
    favorite = Favorite.query.filter_by(
        user_id=user_id, character_id=character_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
        
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

@api.route('/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(user_id, planet_id):
    favorite = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
        
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200