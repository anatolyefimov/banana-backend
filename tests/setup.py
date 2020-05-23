import unittest

import app as app_module

class TestSetup(unittest.TestCase):
    def setUp(self):
        self.app = app_module.app.test_client()
        app_module.app.config.from_mapping(
            MONGO_URI="mongodb://localhost:27017/banana-test",
            SECRET_KEY='test'
        )
        app_module.mongo.init_app(app_module.app)
        app_module.mongo.db.users.drop()
        app_module.mongo.db.baskets.drop()
        app_module.mongo.db.products.drop()
        print('init app and new DB banana-test')

    def tearDown(self):
        app_module.mongo.db.users.drop()
        app_module.mongo.db.baskets.drop()
        app_module.mongo.db.products.drop()
        print("close app")
