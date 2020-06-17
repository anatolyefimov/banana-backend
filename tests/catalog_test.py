import json

import app as app_module
from app.db.product import new_product
from tests.setup import TestSetup


shoes1 = new_product(title='shoes1', price=1, category='shoes')
shoes2 = new_product(title='shoes2', price=1, category='shoes')
trousers1 = new_product(title='trousers1', price=1, category='trousers')
trousers2 = new_product(title='trousers2', price=1, category='trousers')


class CatalogTestCase(TestSetup):

    def test_catalog_get_all(self):
        product1 = new_product(title='test1', price=1)
        product2 = new_product(title='test2', price=2)
        app_module.mongo.db.catalog.insert_one(product1)
        app_module.mongo.db.catalog.insert_one(product2)

        catalog = self.app.get('/catalog').get_json()

        ans1 = json.loads(catalog[0])
        ans2 = json.loads(catalog[1])
        assert ans1['title'] == 'test1' and ans1['price'] == 1
        assert ans2['title'] == 'test2' and ans2['price'] == 2

    def test_catalog_get_category(self):
        app_module.mongo.db.catalog.insert_many([shoes1, shoes2, trousers1, trousers2])

        shoes_catalog = self.app.get('/catalog?category=shoes')
        shoes_catalog = shoes_catalog.get_json()

        assert len(shoes_catalog) == 2
        for item in shoes_catalog:
            assert json.loads(item)['category'] == 'shoes'

    def test_create_garbage_product(self):
        self.app.post('/create_garbage_product', json={})
        self.app.post('/create_garbage_product', json={'title': 'tolya', 'price': '100'})
        self.app.post('/create_garbage_product', json={'title': 'aydar', 'price': '100'})

        ans = self.app.get('/catalog').get_json()
        assert len(ans) == 3

        assert json.loads(ans[1])['title'] == 'tolya'
        assert json.loads(ans[2])['title'] == 'aydar'

    def test_get_products_by_ids(self):
        shoes1_id = str(app_module.mongo.db.catalog.insert_one(shoes1).inserted_id)
        shoes2_id = str(app_module.mongo.db.catalog.insert_one(shoes2).inserted_id)

        # get one product
        products = self.app.get('/products?id=' + shoes1_id).get_json()
        product0 = json.loads(products[0])
        assert product0['title'] == shoes1['title']

        # get two products with delimiter comma
        products = self.app.get('/products?id=' + shoes1_id + ',' + shoes2_id).get_json()
        product1 = json.loads(products[1])
        assert product1['title'] == shoes2['title']
