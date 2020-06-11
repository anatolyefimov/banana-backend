import jwt
from bson import ObjectId

import app as app_module
from app.db.product import new_product
from tests.setup import TestSetup

TEST_PASSWORD = 'test_pass'
TEST_USERNAME = 'test_user'
credentials_json = {'username': TEST_USERNAME, 'password': TEST_PASSWORD}

product1 = new_product(name='test1', price=1)
product2 = new_product(name='test2', price=2)


class BasketTestCase(TestSetup):

    def test_add_product_to_basket(self):
        access_token, product1_id, product2_id = self._auth_preparation()
        res2 = self.app.post(
            '/add_to_basket',
            json={'product_id': product2_id, 'access_token': access_token}).get_json()

        basket = res2['basket']
        total_sum = res2['total_sum']

        assert basket[product1_id] == 1
        assert basket[product2_id] == 2
        # 1*1 + 2*2 = 5
        assert total_sum == 5

        # check values in DB
        basket_db, total_sum_db = self._get_basket_and_total_sum_from_db(access_token)
        assert basket_db == basket
        assert total_sum_db == total_sum

    def test_remove_product_from_basket(self):
        access_token, product1_id, product2_id = self._auth_preparation()
        res2 = self.app.post(
            '/remove_from_basket',
            json={'product_id': product2_id, 'access_token': access_token}).get_json()
        basket = res2['basket']
        total_sum = res2['total_sum']

        assert basket[product1_id] == 1
        assert product2_id not in basket
        assert total_sum == 1

        res2 = self.app.post(
            '/remove_from_basket',
            json={'product_id': product1_id, 'access_token': access_token}).get_json()
        assert not res2['basket']
        assert res2['total_sum'] == 0

        basket_db, total_sum_db = self._get_basket_and_total_sum_from_db(access_token)
        assert not basket_db
        assert total_sum_db == 0

    def test_clear_basket(self):
        access_token, _, _ = self._auth_preparation()

        res2 = self.app.post('/clear_basket', json={'access_token': access_token}).get_json()
        assert not res2['basket']
        assert res2['total_sum'] == 0

        basket_db, total_sum_db = self._get_basket_and_total_sum_from_db(access_token)
        assert not basket_db
        assert total_sum_db == 0

    def _auth_preparation(self):
        self.app.post('/register', json=credentials_json)
        res = self.app.post('/login', json=credentials_json).get_json()
        access_token = res['access_token']

        product1_id = str(app_module.mongo.db.catalog.insert_one(product1).inserted_id)
        product2_id = str(app_module.mongo.db.catalog.insert_one(product2).inserted_id)

        self.app.post('/add_to_basket',
                      json={'product_id': product1_id, 'access_token': access_token})
        self.app.post('/add_to_basket',
                      json={'product_id': product2_id, 'access_token': access_token})

        return access_token, product1_id, product2_id

    @staticmethod
    def _get_basket_and_total_sum_from_db(access_token):
        user_id = jwt.decode(
            access_token, app_module.app.config['SECRET_KEY'], algorithms=['HS256'])['_id']
        user = app_module.mongo.db.users.find_one({'_id': ObjectId(user_id)})

        return user['basket'], user['total_sum']
