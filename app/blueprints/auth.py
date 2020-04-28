from flask import (
    Blueprint, request, session
)
from werkzeug.security import (
    check_password_hash, generate_password_hash
)
from bson.objectid import ObjectId

from flaskr.db.mongo import mongo
from flaskr.db.user import new_user


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
    mongo.db.users.insert_one(user)

    return {
        'message': 'User created successfully',
    }, 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'username': data['username']})
    
    if user is None or  not check_password_hash(user['password'], data['password']):
        user = new_user()
        user['isLoggedIn'] = False

        return user
    session['user_id'] = str(user['_id'])
    user['_id'] = str(user['_id'])
    user.pop('password')
    user['isLoggedIn'] = True
    return user, 200

@bp.route('/logout')
def logout():
    session.clear()
    return {
        'message': 'User succecfully logged out'
    } , 200