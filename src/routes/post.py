from flask import jsonify, Blueprint

api = Blueprint('api/post', __name__)

@api.route('/')
def get_posts():
    return jsonify('get posts'), 200