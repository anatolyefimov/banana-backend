import os

from flask import (
    Blueprint, request
)
from flask import current_app as app
from werkzeug.security import (
    check_password_hash, generate_password_hash
)
import jwt

from app.db.mongo import mongo
from app.db.user import new_user



bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if mongo.db.users.find_one({'username': data['username']}):
        return {
            'message': 'This username is already taken.'
        }, 409
    
    user = new_user(data['username'])
    user['password'] = generate_password_hash(data['password'])
    user_id = str(mongo.db.users.insert_one(user).inserted_id)
    encoded_jwt = jwt.encode({ '_id' : user_id }, app.config['SECRET_KEY'], algorithm='HS256')
    

    return {
        'auth_token': encoded_jwt.decode('utf-8'),
    }, 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'username': data['username']})
    
    if user is None or  not check_password_hash(user['password'], data['password']):
        return {
            'auth_token': None
        }, 200

    encoded_jwt = jwt.encode({ '_id' : str(user['_id']) }, app.config['SECRET_KEY'], algorithm='HS256')
    encoded_jwt = encoded_jwt.decode('utf-8')
    return {
        'auth_token': encoded_jwt
    }, 200

@bp.route('/')
def hello():
    return 'hello' , 200
