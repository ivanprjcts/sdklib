import unittest

from tests.sample_sdk import SampleSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # SampleSdk.set_proxy("localhost:8888")
        cls.api = SampleSdk()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_search(self):
        status, response, headers = self.api.get_restaurants()
        self.assertEqual(status, 200)
        res_data = response.get_data()
        self.assertIn("results", res_data)
        self.assertTrue(isinstance(res_data["results"], list))
