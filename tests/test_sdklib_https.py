import unittest

from tests.sample_sdk_https import SampleHttpsHttpSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # SampleHttpsHttpSdk.set_default_proxy("localhost:8080")
        cls.api = SampleHttpsHttpSdk()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ignore_warnings(self):
        """
        Check that no warnings are printed
        """
        SampleHttpsHttpSdk.ignore_warnings = True
        api = SampleHttpsHttpSdk()
        api.get_ivanprjcts()
