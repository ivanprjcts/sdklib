import io
import json

from xml.etree import ElementTree

from sdklib.http.session import Cookie
from sdklib.util.structures import xml_string_to_dict


class HttpResponse(io.IOBase):

    def __init__(self, resp):
        self.urllib3_response = resp
        self._cookie = None
        self.file = None

    @property
    def data(self):
        data = self.urllib3_response.data
        try:
            data = data.decode()
            pass
        except:
            data = data
        try:
            return json.loads(data)
        except:
            pass
        try:
            return xml_string_to_dict(data)
        except:
            return data

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

    @property
    def xml(self):
        data = self.urllib3_response.data
        return ElementTree.fromstring(data)

    @property
    def raw(self):
        return self.urllib3_response.data
