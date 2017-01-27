import json

from xml.etree import ElementTree

from sdklib.compat import convert_bytes_to_str
from sdklib.http.session import Cookie
from sdklib.util.structures import xml_string_to_dict, CaseInsensitiveDict
from sdklib.html import HTML


class AbstractHttpResponse(object):
    """
    Wrapper of Urllib3 HTTPResponse class needed to implement any HttpSdk response class.

    See `Urllib3 <http://urllib3.readthedocs.io/en/latest/user-guide.html#response-content>`_.
    """
    def __init__(self, resp):
        self.urllib3_response = resp
        self._cookie = None
        self.file = None

    @property
    def cookie(self):
        if not self._cookie:
            self._cookie = Cookie(self.headers)
        else:
            self._cookie.load_from_headers(self.headers)
        return self._cookie

    @property
    def headers(self):
        """
        Returns a dictionary of the response headers.
        """
        return self.urllib3_response.getheaders()


class HttpResponse(AbstractHttpResponse):
    """
    Wrapper of Urllib3 HTTPResponse class.

    See `Urllib3 <http://urllib3.readthedocs.io/en/latest/user-guide.html#response-content>`_.
    """
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

    def getheader(self, name, default=None):
        """
        Returns a given response header.
        """
        return self.urllib3_response.getheader(name, default)

    @property
    def json(self):
        data = self.urllib3_response.data
        return json.loads(convert_bytes_to_str(data))

    @property
    def case_insensitive_dict(self):
        return CaseInsensitiveDict(self.json)

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


class Error(object):
    def __init__(self, json_data):
        self.json = json_data
        self.case_insensitive_dict = CaseInsensitiveDict(self.json)

    @property
    def code(self):
        return self.case_insensitive_dict['code'] if "code" in self.case_insensitive_dict else None

    @property
    def message(self):
        return self.case_insensitive_dict['message'] if "message" in self.case_insensitive_dict else None

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, value):
        self._json = value if isinstance(value, dict) else dict()

    def __repr__(self):
        return json.dumps(self.json)

    def __str__(self):
        return self.__repr__()


class Api11PathsResponse(AbstractHttpResponse):
    """
    This class models a response from any of the endpoints in most of 11Paths APIs.

    It consists of a "data" and an "error" elements. Although normally only one of them will be present, they are not
    mutually exclusive, since errors can be non fatal, and therefore a response could have valid information in the data
    field and at the same time inform of an error.
    """
    @property
    def json(self):
        data = self.urllib3_response.data
        return json.loads(convert_bytes_to_str(data))

    @property
    def case_insensitive_dict(self):
        return CaseInsensitiveDict(self.json)

    @property
    def data(self):
        """
        :return: data part of the API response into a dictionary
        """
        return self.case_insensitive_dict.get("data", None)

    @property
    def error(self):
        """
        @return Error the error part of the API response, consisting of an error code and an error message
        """
        return Error(self.case_insensitive_dict["error"]) if self.case_insensitive_dict.get("error", None) is not None \
            else None
