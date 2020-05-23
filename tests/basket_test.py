import app as app_module
import json
from app.db.product import new_product
from tests.setup import TestSetup

TEST_PASSWORD = 'test_pass'
TEST_USERNAME = 'test_user'


class BasketTestCase(TestSetup):

    def test_add_product_to_basket(self):
        self.app.post('/register', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        res = self.app.post('/login', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        res_data = res.get_json()
        access_token = res_data['access_token']

        product1 = new_product(name='test1', price=1)
        product2 = new_product(name='test2', price=2)
        product1_id = str(app_module.mongo.db.products.insert_one(product1).inserted_id)
        product2_id = str(app_module.mongo.db.products.insert_one(product2).inserted_id)

        self.app.post('/add_to_basket', json={'product_id': product1_id, 'access_token': access_token})
        self.app.post('/add_to_basket', json={'product_id': product2_id, 'access_token': access_token})
        res2 = self.app.post('/add_to_basket', json={'product_id': product2_id, 'access_token': access_token})

        basket = res2.get_json()['basket']
        print('basket: ', basket)
        assert basket[product1_id] == 1
        assert basket[product2_id] == 2
