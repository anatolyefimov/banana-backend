import os

from flask import (
    Blueprint, request
)

bp = Blueprint('products', __name__)

@bp.route('/get_products')
def get_products():
    