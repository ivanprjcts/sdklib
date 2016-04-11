import unittest

from tests.sample_sdk_https import SampleHttpsSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # SampleSdk.set_proxy("localhost:8888")
        cls.api = SampleHttpsSdk()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_products(self):
        status, response, headers = self.api.get_products()
        self.assertEqual(status, 200)
        res_data = response.get_data()
        self.assertTrue(isinstance(res_data, list))
