import os

from flask import Flask
from app.blueprints.auth import bp as auth_bp
from app.blueprints.user import bp as user_bp
from app.blueprints.products import bp as products_bp
from app.blueprints.basket import bp as basket_bp

from app.db.mongo import mongo

app = Flask(__name__, instance_relative_config=True)
mongo_uri = os.getenv('DB') if os.getenv('DB') else 'mongodb://localhost:27017/banana'
app.config.from_mapping(
        MONGO_URI=mongo_uri,
        SECRET_KEY=os.getenv('SECRET_KEY'),
)

mongo.init_app(app)
from app.db.product import new_product
app.logger.info(mongo)
app.logger.info(mongo.db)
app.logger.info(mongo.db.products)
app.logger.info(mongo.db.users)

product1 = new_product()
app.logger.info(product1)

mongo.db.products.insert_one(product1)

app.logger.info('Initialize class PyMongo')
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(products_bp)
app.register_blueprint(basket_bp)
