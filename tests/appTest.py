import app
import unittest
from werkzeug.security import (
    check_password_hash
)

TEST_PASSWORD = 'test_pass'
TEST_USERNAME = 'test_user'

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        app.app.config.from_mapping(
            MONGO_URI="mongodb://localhost:27017/banana-test",
            SECRET_KEY='test'
        )
        app.mongo.init_app(app.app)
        print('init app and new DB banana-test')

    def tearDown(self):
        print("close app")

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'hello' in str(rv.data)
        assert rv.status_code == 200

    def test_reg(self):
        app.mongo.db.users.drop()
        rv = self.app.post('/register', json = {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        test_user = app.mongo.db.users.find_one({'username': TEST_USERNAME})
        print(test_user)

        assert test_user.get('username') == TEST_USERNAME
        assert check_password_hash(test_user.get('password'), TEST_PASSWORD) == True
        assert rv.status_code == 201

    def test_full_cycle(self):
        app.mongo.db.users.drop()
        self.app.post('/register', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        rv = self.app.post('/login', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})

        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()
