from flask import (
    Blueprint, request, jsonify
)
from app.db.mongo import mongo
from bson import ObjectId, json_util

from app.db.product import new_product

CATEGORIES_LIST = {'trousers', 't-shirt', 'shoes'}

bp = Blueprint('catalog', __name__)


@bp.route('/catalog')
def get_products():
    """
        Returns: all products list if category not specified, else all products by concrete category

        /catalog?category=shoes - return all products with category shoes
        /catalog - return all products
    """
    category = request.args.get('category')
    if category in CATEGORIES_LIST:
        catalog = mongo.db.catalog.find({'category': category})
    else:
        catalog = mongo.db.catalog.find({})

    ans = []
    for product in catalog:
        ans.append(json_util.dumps(product))

    return jsonify(ans), 200


@bp.route('/product')
def get_product_by_id():
    product_id = request.args.get('id')
    product = mongo.db.catalog.find_one({'_id': ObjectId(product_id)})

    return jsonify(json_util.dumps(product)), 200


@bp.route('/create_garbage_product', methods=['POST'])
def create_garbage_product():
    """
        utils method for testing catalog and filling database
    """
    data = request.get_json()
    name = data.get('name', 'foo')
    category = data.get('category', 'shoes')
    price = data.get('price', 1)
    image_url = data.get('image_url', '')

    product = new_product(name, category, price, image_url)
    product_id = str(mongo.db.catalog.insert_one(product).inserted_id)

    return jsonify(product_id), 201
