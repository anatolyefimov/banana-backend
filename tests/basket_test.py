import app as app_module
from app.db.product import new_product
from tests.setup import TestSetup

TEST_PASSWORD = 'test_pass'
TEST_USERNAME = 'test_user'

product1 = new_product(name='test1', price=1)
product2 = new_product(name='test2', price=2)


class BasketTestCase(TestSetup):

    def test_add_product_to_basket(self):
        access_token, product1_id, product2_id = self._auth_preparation()
        res2 = self.app.post('/add_to_basket', json={'product_id': product2_id, 'access_token': access_token}).get_json()

        basket = res2['basket']
        total_sum = res2['total_sum']

        assert basket[product1_id] == 1
        assert basket[product2_id] == 2
        # 1*1 + 2*2 = 5
        assert total_sum == 5

    def test_delete_product_from_basket(self):
        access_token, product1_id, product2_id = self._auth_preparation()
        res2 = self.app.post('/remove_from_basket', json={'product_id': product2_id, 'access_token': access_token}).get_json()
        basket = res2['basket']
        total_sum = res2['total_sum']

        assert basket[product1_id] == 1
        assert product2_id not in basket
        assert total_sum == 1

        res2 = self.app.post('/remove_from_basket', json={'product_id': product1_id, 'access_token': access_token}).get_json()
        basket = res2['basket']
        total_sum = res2['total_sum']

        assert not basket
        assert total_sum == 0

    def _auth_preparation(self):
        self.app.post('/register', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        res = self.app.post('/login', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        res_data = res.get_json()
        access_token = res_data['access_token']

        product1_id = str(app_module.mongo.db.catalog.insert_one(product1).inserted_id)
        product2_id = str(app_module.mongo.db.catalog.insert_one(product2).inserted_id)

        self.app.post('/add_to_basket', json={'product_id': product1_id, 'access_token': access_token})
        self.app.post('/add_to_basket', json={'product_id': product2_id, 'access_token': access_token})

        return access_token, product1_id, product2_id
