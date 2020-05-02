import unittest

from werkzeug.security import check_password_hash

import app as app_module

TEST_PASSWORD = 'test_pass'
TEST_USERNAME = 'test_user'

class BananaOnStartTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app_module.app.test_client()
        app_module.app.config.from_mapping(
            MONGO_URI="mongodb://localhost:27017/banana-test",
            SECRET_KEY='test'
        )
        app_module.mongo.init_app(app_module.app)
        print('init app and new DB banana-test')

    def tearDown(self):
        print("close app")

    def test_empty_db(self):
        res = self.app.get('/')
        assert 'hello' in str(res.data)
        assert res.status_code == 200

    def test_registration(self):
        app_module.mongo.db.users.drop()
        res = self.app.post(
            '/register',
            json={
                'username': TEST_USERNAME,
                'password': TEST_PASSWORD
            }
        )
        test_user = app_module.mongo.db.users.find_one({'username': TEST_USERNAME})
        print(test_user)

        assert test_user.get('username') == TEST_USERNAME
        assert check_password_hash(test_user.get('password'), TEST_PASSWORD)
        assert res.status_code == 201

    def test_full_cycle(self):
        app_module.mongo.db.users.drop()
        self.app.post('/register', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        res = self.app.post('/login', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        logined_user = res.get_json()

        assert res.status_code == 200
        assert logined_user['username'] == TEST_USERNAME
        assert logined_user['isLoggedIn']

        res2 = self.app.get('/logout')
        assert res2.status_code == 200
        assert res2.get_json()['message'] == 'User successfully logged out'


if __name__ == '__main__':
    unittest.main()
