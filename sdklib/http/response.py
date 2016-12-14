import io
import json

from xml.etree import ElementTree

from sdklib.http.session import Cookie
from sdklib.util.structures import xml_string_to_dict
from sdklib.html import HTML


class HttpResponse(object):
    """
    Wrapper of Urllib3 HTTPResponse class.

    See `Urllib3 <http://urllib3.readthedocs.io/en/latest/user-guide.html#response-content>`_.
    """

    def __init__(self, resp):
        self.urllib3_response = resp
        self._cookie = None
        self.file = None

    @property
    def data(self):
        data = self.urllib3_response.data
        try:
            data = data.decode()
        except:
            pass
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
        """
        HTTP Status Code.
        """
        return self.urllib3_response.status

    @property
    def reason(self):
        """
        HTTP Reason phrase.
        """
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
    def json(self):
        data = self.urllib3_response.data
        return json.loads(data)

    @property
    def xml(self):
        data = self.urllib3_response.data
        return ElementTree.fromstring(data)

    @property
    def raw(self):
        """
        Returns urllib3 response data.
        """
        return self.urllib3_response.data

    @property
    def html(self):
        """
        Returns HTML response data.
        """
        return HTML(self.urllib3_response.data)
