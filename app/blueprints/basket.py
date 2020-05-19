from flask import (
    Blueprint, request
)
from app.db.mongo import mongo
from app.db.user import new_user

bp = Blueprint('basket', __name__)

@bp.route('/get_basket')
def get_basket():
    pass


@bp.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    data = request.get_json()
    product = mongo.db.products.find_one({'productId': data['productId']})
