import io
import json

from sdklib.http.session import Cookie


class HttpResponse(io.IOBase):

    def __init__(self, resp):
        self.urllib3_response = resp
        self._cookie = None
        self.file = None

    @property
    def data(self):
        data = self.urllib3_response.data
        try:
            decoded_data = data.decode()
        except:
            decoded_data = data
        try:
            return json.loads(decoded_data)
        except:
            return decoded_data

    @property
    def status(self):
        return self.urllib3_response.status

    @property
    def reason(self):
        return self.urllib3_response.reason

    @property
    def headers(self):
        """
        Returns a dictionary of the response headers.
        """
        return self.urllib3_response.getheaders()

    @property
    def cookie(self):
        if not self._cookie:
            self._cookie = Cookie(self.headers)
        else:
            self._cookie.load_from_headers(self.headers)
        return self._cookie

    def getheader(self, name, default=None):
        """
        Returns a given response header.
        """
        return self.urllib3_response.getheader(name, default)
