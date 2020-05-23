import app as app_module
import json
from app.db.product import new_product
from tests.setup import TestSetup

TEST_PASSWORD = 'test_pass'
TEST_USERNAME = 'test_user'


class ProductsTestCase(TestSetup):

    def test_get_products(self):
        self.app.post('/register', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        res = self.app.post('/login', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        assert res.status_code == 200

        product1 = new_product(name='test1', price=1)
        product2 = new_product(name='test2', price=2)
        app_module.mongo.db.products.insert_one(product1)
        app_module.mongo.db.products.insert_one(product2)

        prod = self.app.get('/get_products')
        prod = prod.get_json()

        ans1 = json.loads(prod['ans'][0])
        ans2 = json.loads(prod['ans'][1])
        assert ans1['name'] == 'test1' and ans1['price'] == 1
        assert ans2['name'] == 'test2' and ans2['price'] == 2

    def test_get_products_ids(self):
        self.app.post('/register', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        self.app.post('/login', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})

        product1 = new_product(name='test1', price=1)
        product2 = new_product(name='test2', price=2)
        app_module.mongo.db.products.insert_one(product1)
        app_module.mongo.db.products.insert_one(product2)

        products = self.app.get('/get_products_ids')
        products = products.get_json()['ans']
        print(products)
        assert products[0]

        res = self.app.post('/get_product', json={'id': products[0]})
        ans1 = json.loads(res.get_json()['ans'])
        print(ans1)
        assert ans1['name'] == 'test1'

    def test_create_garbage_product(self):
        self.app.post('/create_garbage_product', json={})
        self.app.post('/create_garbage_product', json={})
        self.app.post('/create_garbage_product', json={})

        res = self.app.get('/get_products_ids')
        products_ids = res.get_json()['ans']
        assert len(products_ids) == 3
