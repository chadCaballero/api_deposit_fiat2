import os
import apps as flaskr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()

# import unittest
# import requests
# import json
# import sys
#
#
# class TestFlaskApiUsingRequests(unittest.TestCase):
#     def commissions(self):
#         response = requests.get('http://localhost:8000/v1/commissions/money/9/countries/2/payments/2/collectors/12',
#                                 headers={'Content-Type': 'application/json'})
#         self.assertEqual(response.json(), {'hello': 'world'})
#
#
# class TestFlaskApi(unittest.TestCase):
#     def setUp(self):
#         self.app = flaskapi.app.test_client()
#
#     def test_hello_world(self):
#         response = self.app.get('/')
#         self.assertEqual(json.loads(response.get_data().decode(sys.getdefaultencoding())), {'hello': 'world'})
#
#
# if __name__ == "__main__":
#     unittest.main()