import unittest

from sdklib.test.rrserver import manager, RequestResponseHandler
from sdklib.util.files import read_file_as_string

from tests.sample_sdk import SampleSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        RequestResponseHandler.add_request_response(request=read_file_as_string('requests/get_restaurants.txt'),
                                                    response=read_file_as_string('responses/get_restaurants.txt'))
        RequestResponseHandler.add_request_response(request=read_file_as_string('requests/create_restaurant.txt'))
        RequestResponseHandler.add_request_response(request=read_file_as_string('requests/login.txt'))
        host, port = manager.start_rrserver()

        # SampleSdk.set_default_proxy("http://localhost:8080")
        SampleSdk.set_default_host("http://%s:%s" % (host, port))
        cls.api = SampleSdk()

    @classmethod
    def tearDownClass(cls):
        manager.close_rrserver()

    def test_get_restaurants(self):
        response = self.api.get_restaurants()
        self.assertEqual(response.status, 200)
        self.assertIn("results", response.data)
        self.assertTrue(isinstance(response.data["results"], list))

    def test_login(self):
        response = self.api.login(username='user', password='123')
        self.assertEqual(response.status, 200)

    def test_create_restaurant(self):
        response = self.api.create_restaurant("mi restaurante", "algo", "Madrid")
        self.assertEqual(response.status, 200)
