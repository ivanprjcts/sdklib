from sdklib.http import HttpSdk


class SampleHttpsHttpSdk(HttpSdk):

    DEFAULT_HOST = "https://www.google.com"

    API_IVANPRJCTS_PATH = "/ivanprjcts"

    def get_ivanprjcts(self):
        return self.get(self.API_IVANPRJCTS_PATH)
