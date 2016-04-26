import unittest

from tests.sample_sdk import SampleSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SampleSdk.set_default_proxy("http://localhost:8080")
        cls.api = SampleSdk()


    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_restaurants(self):
        response = self.api.get_restaurants()
        self.assertEqual(response.status, 200)
        self.assertIn("results", response.data)
        self.assertTrue(isinstance(response.data["results"], list))
