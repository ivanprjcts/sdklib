import unittest

from sdklib.test.rrserver import RRServer
from sdklib.util.files import read_file_as_string

from tests.sample_sdk import SampleHttpSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        RRServer.manager.add_request_response(request=read_file_as_string('tests/requests/get_restaurants.txt'),
                                              response=read_file_as_string('tests/responses/get_restaurants.txt'))
        RRServer.manager.add_request_response(request=read_file_as_string('tests/requests/create_restaurant.txt'))
        RRServer.manager.add_request_response(request=read_file_as_string('tests/requests/login.txt'))
        RRServer.manager.add_request_response(request=read_file_as_string('tests/requests/update_restaurant.txt'))
        host, port = RRServer.manager.start_rrserver()

        # SampleHttpSdk.set_default_proxy("http://localhost:8080")
        SampleHttpSdk.set_default_host("http://%s:%s" % (host, port))
        cls.api = SampleHttpSdk()

    @classmethod
    def tearDownClass(cls):
        RRServer.manager.close_rrserver()

    def test_get_restaurants(self):
        response = self.api.get_restaurants()
        self.assertEqual(response.status, 200)
        self.assertIn("results", response.data)
        self.assertTrue(isinstance(response.data["results"], list))

    def _test_login(self):
        response = self.api.login(username='user', password='123')
        self.assertEqual(response.status, 200)

    def _test_create_restaurant(self):
        response = self.api.create_restaurant("mi restaurante", "algo", "Madrid")
        self.assertEqual(response.status, 200)

    def _test_update_restaurant(self):
        response = self.api.update_restaurant("mi restaurante", "tests/resources/file.png", "algo", "Madrid")
        self.assertEqual(response.status, 200)
