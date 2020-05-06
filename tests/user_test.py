import jwt

import app as app_module
from tests.setup import TestSetup

TEST_PASSWORD = 'test_pass'
TEST_USERNAME = 'test_user'

class UserTestCase(TestSetup):
    def test_get_user_data(self):
        user_id = str(app_module.mongo.db.users.insert_one({
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD
        }).inserted_id)

        encoded_user_id = jwt.encode(
            {
                '_id': user_id
            },
            app_module.app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        res = self.app.post(
            '/get_user_data',
            json={
                'accessToken': encoded_user_id.decode('utf-8')
            }
        )
        res = res.get_json()

        assert res['username'] == TEST_USERNAME
