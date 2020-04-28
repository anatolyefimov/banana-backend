import os

from flask import Flask
from app.blueprints.auth import bp as auth_bp

from app.db.mongo import mongo

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        MONGO_URI = "mongodb://localhost:27017/banana",
        SECRET_KEY='dev',
)

mongo.init_app(app)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

app.register_blueprint(auth_bp)





