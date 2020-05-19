import os

from flask import (
    Blueprint, request
)
from app.db.mongo import mongo

bp = Blueprint('products', __name__)

@bp.route('/get_products')
def get_products():
    all_products = mongo.db.products.find({})
    print(all_products)
    for doc in all_products:
        print(doc)
    return 'ok', 200
