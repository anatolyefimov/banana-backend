from flask import (
    Blueprint, request
)
from flask import current_app as app
import jwt
from bson.objectid import ObjectId

from app.db.mongo import mongo

bp = Blueprint('user', __name__)

@bp.route('/get_user_data', methods=['POST'])
def get_user_data():
    accessToken = request.get_json()['accessToken']
    user_id = jwt.decode(accessToken, app.config['SECRET_KEY'], algorithms=['HS256'])['_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

    return {
        'username': user['username']
    }, 200

    


