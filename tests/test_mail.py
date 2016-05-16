import unittest

from sdklib.mail import (
    GmailPOPlSdk, GmailIMAPlSdk, OutlookPOPlSdk, OutlookIMAPlSdk, OutlookOffice365POPlSdk, OutlookOffice365IMAPlSdk,
    GmailSMTPlSdk
)


class TestGmailPOPSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = GmailPOPlSdk('sdklib.test', 'sdklib12345678')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_read_all_mails(self):
        messages = self.api.read_all_mails()
        print messages
        for m in messages:
            print dir(m)


class TestOutlookPOPSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = OutlookPOPlSdk('sdklib.test@outlook.com', 'sdklib12345678')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_read_all_mails(self):
        messages = self.api.read_all_mails()
        print messages
        for m in messages:
            print m


class TestOutlookOffice365POPSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = OutlookOffice365POPlSdk('USER@ACCOUNT.com', 'PASSWORD')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_read_all_mails(self):
        messages = self.api.read_all_mails()
        print messages
        for m in messages:
            print m


class TestGmailIMAPSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = GmailIMAPlSdk('sdklib.test', 'sdklib12345678')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_read_all_mails(self):
        messages = self.api.read_all_mails()
        for m in messages:
            print m


class TestOutlookIMAPSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = OutlookIMAPlSdk('sdklib.test@outlook.com', 'sdklib12345678')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_read_all_mails(self):
        messages = self.api.read_all_mails()
        for m in messages:
            print m


class TestOutlookOffice365IMAPSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = OutlookOffice365IMAPlSdk('USER@ACCOUNT.com', 'PASSWORD.')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_read_all_mails(self):
        messages = self.api.read_all_mails()
        for m in messages:
            print m


class TestGmailSMTPSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = GmailSMTPlSdk('sdklib.test', 'sdklib12345678')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_send_email(self):
        self.api.send_email(to_address="ivanprjcts@gmail.com", subject="Test", message="This is a test.")
