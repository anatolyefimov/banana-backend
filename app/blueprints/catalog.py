import json

from bson import ObjectId
from flask import (
    Blueprint, request, jsonify
)

from app.db.mongo import mongo
from app.db.product import new_product

CATEGORIES_LIST = {'trousers', 'shirts', 'shoes'}

bp = Blueprint('catalog', __name__)


@bp.route('/catalog')
def get_products():
    """
        Returns: all products list if category not specified, else all products by concrete category

        /catalog?category=shoes - return all products with category shoes
        /catalog - return all products
    """
    category = request.args.get('category')
    print(category)
    if category in CATEGORIES_LIST:
        catalog = mongo.db.catalog.find({'category': category})
    else:
        catalog = mongo.db.catalog.find({})

    ans = []
    for product in catalog:
        ans.append(json.dumps(product, default=str, ensure_ascii=False))

    return jsonify(ans), 200


@bp.route('/products')
def get_product_by_ids():
    """
        put id with comma delimiter; don't put comma in the end of query string
        Returns: list of products with specified ids.

        /products?id=1,2 - return list of products with id=1,2
    """
    ids_list = request.args.get('id').split(',')

    ans = []
    for product_id in ids_list:
        product = mongo.db.catalog.find_one({'_id': ObjectId(product_id)})
        ans.append(json.dumps(product, default=str, ensure_ascii=False))

    return jsonify(ans), 200


@bp.route('/create_garbage_product', methods=['POST'])
def create_garbage_product():
    """
        utils method for testing catalog and filling database
    """
    data = request.get_json()
    title = data.get('title', 'foo')
    category = data.get('category', 'shoes')
    price = data.get('price', 1)
    image = data.get('image', '')

    product = new_product(title, category, price, image)
    product_id = str(mongo.db.catalog.insert_one(product).inserted_id)

    return jsonify(product_id), 201


@bp.route('/drop_db')
def drop_db():
    mongo.db.catalog.drop()

    return 'drop', 200
