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
        response = self.api.get_products()
        self.assertEqual(response.status, 200)
        self.assertTrue(isinstance(response.data, list))
