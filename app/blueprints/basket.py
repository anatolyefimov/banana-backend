import jwt
from bson.objectid import ObjectId
from flask import (
    Blueprint, request
)
from flask import current_app as app

from app.db.basket import new_basket
from app.db.mongo import mongo

bp = Blueprint('basket', __name__)

@bp.route('/get_basket')
def get_basket():
    pass


@bp.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    data = request.get_json()
    accessToken = data['accessToken']
    user_id = jwt.decode(accessToken, app.config['SECRET_KEY'], algorithms=['HS256'])['_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

    productId = data['productId']
    product = mongo.db.products.find_one({'_id': ObjectId(productId)})
    print("product")
    print(product)

    basket_id = None
    if user['basket'] is None:
        basket_id = mongo.db.baskets.insert_one(new_basket()).inserted_id
        mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'basket': basket_id}})
    else:
        basket_id = user['basket']
    print(basket_id)
    basket = mongo.db.baskets.find_one({'_id': ObjectId(basket_id)})['productsIds']
    print(basket)

    if basket is None:
        basket = [productId]
    else:
        basket.append(productId)

    mongo.db.baskets.update_one({'_id': ObjectId(basket_id)}, {'$set': {'productsIds': basket}})

    updated_basket = mongo.db.baskets.find_one({'_id': ObjectId(basket_id)})
    print(updated_basket)

    return 'ok', 200


def create_basket():
    mongo.db.baskets.insert_one(new_basket())
