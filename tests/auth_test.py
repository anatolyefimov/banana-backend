import unittest

from werkzeug.security import check_password_hash

import app as app_module
from tests.setup import TestSetup

TEST_PASSWORD = 'test_pass'
TEST_USERNAME = 'test_user'

class AuthenticationTestCase(TestSetup):
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

        res_data = res.get_json()

        assert res.status_code == 200
        assert res_data['auth_token']


if __name__ == '__main__':
    unittest.main()
