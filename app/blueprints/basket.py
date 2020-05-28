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
    '''
    Returns: basket(dict): dict of products #e.g productId -> count

    Parameters:
        product_id(str) : id of product,that user want to basket
        access_token(str) : identification of user

    in basket save only id of product with amount
    '''
    data = request.get_json()
    access_token = data['access_token']
    user_id = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms=['HS256'])['_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

    product_id = data['product_id']
    # don't use but for example
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})

    basket_id = user['basket']
    if basket_id is None:
        basket_id = str(mongo.db.baskets.insert_one(new_basket()).inserted_id)
        mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'basket': basket_id}})

    basket = mongo.db.baskets.find_one({'_id': ObjectId(basket_id)})['products_dict']

    basket = _primitive_add_in_dict(basket, product_id)
    mongo.db.baskets.update_one({'_id': ObjectId(basket_id)}, {'$set': {'products_dict': basket}})

    return {
               'basket': basket,
               'total_sum': calc_total_sum(basket),
           }, 200


def _primitive_add_in_dict(basket, product_id):
    if basket is None:
        basket = {product_id: 1}
    else:
        if product_id in basket:
            basket[product_id] += 1
        else:
            basket[product_id] = 1

    return basket


def calc_total_sum(basket):
    total_sum = 0
    for key in basket:
        total_sum += _get_price_by_id(key) * basket[key]

    return total_sum


def _get_price_by_id(product_id):
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    return product['price']
