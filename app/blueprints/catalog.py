from flask import (
    Blueprint, request
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

    return {
               'ans': ans
           }, 200


@bp.route('/product')
def get_product_by_id():
    product_id = request.args.get('id')
    product = mongo.db.catalog.find_one({'_id': ObjectId(product_id)})

    return {
               'product': json_util.dumps(product)
           }, 200


@bp.route('/create_garbage_product')
def create_garbage_product():
    """
        utils method for testing catalog and filling database
    """
    name = request.args.get('name', default='foo')
    category = request.args.get('category', default='shoes')
    price = request.args.get('price', default=1, type=int)
    image_url = request.args.get('image_url', default='')

    product = new_product(name, category, price, image_url)
    product_id = str(mongo.db.catalog.insert_one(product).inserted_id)

    return {
               'product_id': product_id
           }, 200
