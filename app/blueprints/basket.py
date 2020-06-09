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

    basket = user['basket']
    basket = _primitive_add_in_dict(basket, product_id)

    mongo.db.users.update_one({'_id': ObjectId(user['_id'])}, {'$set': {'basket': basket}})

    return {
               'basket': basket,
               'total_sum': _calc_total_sum(basket),
           }, 200


@bp.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    data = request.get_json()
    access_token = data['access_token']
    product_id = data['product_id']
    user = get_user(access_token)

    basket = user['basket']
    basket = _primitive_remove_from_dict(basket, product_id)

    mongo.db.users.update_one({'_id': ObjectId(user['_id'])}, {'$set': {'basket': basket}})

    return {
               'basket': basket,
               'total_sum': _calc_total_sum(basket),
           }, 200


def _primitive_add_in_dict(basket, product_id):
    if product_id in basket:
        basket[product_id] += 1
    else:
        basket[product_id] = 1

    return basket


def _calc_total_sum(basket):
    total_sum = 0
    for key in basket:
        total_sum += _get_price_by_id(key) * basket[key]

    return total_sum


def _get_price_by_id(product_id):
    product = mongo.db.catalog.find_one({'_id': ObjectId(product_id)})
    return product['price']


def _primitive_remove_from_dict(basket, product_id):
    if basket[product_id] == 1:
        basket.pop(product_id, None)
    else:
        basket[product_id] -= 1

    return basket
