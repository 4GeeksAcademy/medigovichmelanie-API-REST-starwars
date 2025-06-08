from flask import jsonify, Blueprint, request
from models.User import User
from database.db import db

api = Blueprint('api/user', __name__)


@api.route('/', methods=['GET'])
def get_users():
    return jsonify('get users'), 200


@api.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify(f'user not found {user_id}'), 404
    return jsonify(user.serialize())


@api.route('/register', methods=['POST'])
def create_users():
    body = request.get_json()

    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True

    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.serialize()), 200