import json

import app as app_module
from app.db.product import new_product
from tests.setup import TestSetup


class CatalogTestCase(TestSetup):

    def test_catalog_get_all(self):
        product1 = new_product(name='test1', price=1)
        product2 = new_product(name='test2', price=2)
        app_module.mongo.db.catalog.insert_one(product1)
        app_module.mongo.db.catalog.insert_one(product2)

        prod = self.app.get('/catalog').get_json()

        ans1 = json.loads(prod['ans'][0])
        ans2 = json.loads(prod['ans'][1])
        assert ans1['name'] == 'test1' and ans1['price'] == 1
        assert ans2['name'] == 'test2' and ans2['price'] == 2

    def test_catalog_by_categories(self):
        shoes1 = new_product(name='shoes1', price=1, category='shoes')
        shoes2 = new_product(name='shoes2', price=1, category='shoes')
        trousers1 = new_product(name='trousers1', price=1, category='trousers')
        trousers2 = new_product(name='trousers2', price=1, category='trousers')

        app_module.mongo.db.catalog.insert_many([shoes1, shoes2, trousers1, trousers2])

        shoes_catalog = self.app.get('/catalog?category=shoes')
        shoes_catalog = shoes_catalog.get_json()['ans']

        assert len(shoes_catalog) == 2
        for item in shoes_catalog:
            assert json.loads(item)['category'] == 'shoes'

    def test_create_garbage_product(self):
        self.app.get('/create_garbage_product', json={})
        self.app.get('/create_garbage_product?name=tolya&price=100')
        self.app.get('/create_garbage_product?name=aydar&price=100')

        ans = self.app.get('/catalog').get_json()['ans']
        assert len(ans) == 3

        assert json.loads(ans[1])['name'] == 'tolya'
        assert json.loads(ans[2])['name'] == 'aydar'

    def test_get_product_by_id(self):
        shoes1 = new_product(name='shoes1', price=1, category='shoes')
        shoes1_id = str(app_module.mongo.db.catalog.insert_one(shoes1).inserted_id)

        product = self.app.get('/product?id=' + shoes1_id).get_json()['product']
        product = json.loads(product)

        assert product['name'] == shoes1['name']
        assert product['price'] == shoes1['price']
