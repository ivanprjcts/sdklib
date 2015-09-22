import unittest

from sample_sdk import SampleSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SampleSdk.set_proxy("localhost:8888")
        cls.api = SampleSdk()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_search(self):
        status, response, headers = self.api.search("Test", "1.0")
        self.assertEqual(status, 200)
        res_data = response.get_data()
        self.assertIn("responseData", res_data)
        self.assertIn("results", res_data["responseData"])
        self.assertNotEqual(res_data["responseData"]["results"], [])
