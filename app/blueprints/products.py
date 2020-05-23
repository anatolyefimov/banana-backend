from flask import (
    Blueprint, request
)
from app.db.mongo import mongo
from bson import ObjectId, json_util

from app.db.product import new_product

bp = Blueprint('products', __name__)


@bp.route('/get_products')
def get_products():
    all_products = mongo.db.products.find({})
    ans = []
    for doc in all_products:
        ans.append(json_util.dumps(doc))

    return {
               'ans': ans
           }, 200


@bp.route('/get_products_ids')
def get_products_ids():
    all_products = mongo.db.products.find({})
    ans = []
    for product in all_products:
        ans.append(str(product['_id']))

    return {
               'ans': ans
           }, 200


@bp.route('/get_product', methods=['POST'])
def get_product_by_id():
    data = request.get_json()
    product_id = data['id']

    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})

    return {
               'ans': json_util.dumps(product)
           }, 200


@bp.route('/create_garbage_product', methods=['POST'])
def create_garbage_product():
    product1 = new_product()
    product_id = str(mongo.db.products.insert_one(product1).inserted_id)

    return {
               'product_id': product_id
           }, 200
