from bson.objectid import ObjectId
from flask import (
    Blueprint, request
)

from app.blueprints.user import get_user
from app.db.mongo import mongo

bp = Blueprint('basket', __name__)


@bp.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    '''
    Returns: basket(dict): dict of products #e.g productId -> count
             total_sum: integer

    Parameters:
        product_id(str) : id of product,that user want to basket
        access_token(str) : identification of user

    in basket save only id of product with amount
    user includes whole basket
    '''
    data = request.get_json()
    access_token = data['access_token']
    product_id = data['product_id']
    user = get_user(access_token)

    total_sum = user['total_sum']
    basket = user['basket']
    basket, total_sum = _add_product(basket, product_id, total_sum)

    mongo.db.users.update_one({'_id': ObjectId(user['_id'])},
                              {'$set': {'basket': basket, 'total_sum': total_sum}})

    return {
               'basket': basket,
               'total_sum': total_sum
           }, 200


@bp.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    data = request.get_json()
    access_token = data['access_token']
    product_id = data['product_id']
    user = get_user(access_token)

    total_sum = user['total_sum']
    basket = user['basket']
    basket, total_sum = _remove_product(basket, product_id, total_sum)

    mongo.db.users.update_one({'_id': ObjectId(user['_id'])},
                              {'$set': {'basket': basket, 'total_sum': total_sum}})

    return {
               'basket': basket,
               'total_sum': total_sum
           }, 200


def _add_product(basket, product_id, total_sum):
    if product_id in basket:
        basket[product_id] += 1
    else:
        basket[product_id] = 1

    total_sum += _get_price_by_id(product_id)

    return basket, total_sum


def _remove_product(basket, product_id, total_sum):
    if basket[product_id] == 1:
        basket.pop(product_id, None)
    else:
        basket[product_id] -= 1

    total_sum -= _get_price_by_id(product_id)

    return basket, total_sum


def _get_price_by_id(product_id):
    product = mongo.db.catalog.find_one({'_id': ObjectId(product_id)})
    return product['price']
