import os

from flask import Flask
from app.blueprints.auth import bp as auth_bp
from app.blueprints.user import bp as user_bp
from app.blueprints.catalog import bp as catalog_bp
from app.blueprints.basket import bp as basket_bp

from app.db.mongo import mongo

app = Flask(__name__, instance_relative_config=True)
mongo_uri = os.getenv('DB') if os.getenv('DB') else 'mongodb://localhost:27017/banana'
app.config.from_mapping(
        MONGO_URI=mongo_uri,
        SECRET_KEY=os.getenv('SECRET_KEY'),
)

mongo.init_app(app)
app.logger.info('Initialize class PyMongo')
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(basket_bp)
