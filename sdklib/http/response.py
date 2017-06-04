import json

from xml.etree import ElementTree

from sdklib.compat import convert_bytes_to_str
from sdklib.http.session import Cookie
from sdklib.util.structures import xml_string_to_dict, CaseInsensitiveDict
from sdklib.html import HTML


class JsonResponseMixin(object):
    _body = ""

    @property
    def json(self):
        try:
            return json.loads(convert_bytes_to_str(self._body))
        except:
            return dict()

    @property
    def case_insensitive_dict(self):
        return CaseInsensitiveDict(self.json)


class Response(JsonResponseMixin):
    def __init__(self, headers=None, status=None, status_text=None, http_version=None, body=None):
        self.headers = headers
        self.status = status
        self.status_text = status_text
        self.http_version = http_version
        self.body = body
        self._cookie = None

    @property
    def headers(self):
        """
        Returns a dictionary of the response headers.
        """
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value or {}

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def status_text(self):
        return self._status_text

    @status_text.setter
    def status_text(self, value):
        self._status_text = value

    @property
    def http_version(self):
        return self._http_version

    @http_version.setter
    def http_version(self, value):
        self._http_version = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def xml(self):
        return ElementTree.fromstring(self.body)

    @property
    def raw(self):
        """
        Returns urllib3 response data.
        """
        return self.body

    @property
    def html(self):
        """
        Returns HTML response data.
        """
        return HTML(self.body)

    @property
    def data(self):
        data = self.body
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


class AbstractBaseHttpResponse(object):
    """
    Wrapper of Urllib3 HTTPResponse class needed to implement any HttpSdk response class.

    See `Urllib3 <http://urllib3.readthedocs.io/en/latest/user-guide.html#response-content>`_.
    """
    urllib3_response = None
    _cookie = None

    def __init__(self, resp):
        self.urllib3_response = resp

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


class HttpResponse(Response, AbstractBaseHttpResponse):
    """
    Wrapper of Urllib3 HTTPResponse class compatible with AbstractBaseHttpResponse.

    See `Urllib3 <http://urllib3.readthedocs.io/en/latest/user-guide.html#response-content>`_.
    """
    def __init__(self, resp):
        self.urllib3_response = resp
        super(HttpResponse, self).__init__(
            headers=self.urllib3_response.getheaders(),
            status=self.urllib3_response.status,
            status_text=self.urllib3_response.reason,
            body=self.urllib3_response.data
        )

    @property
    def reason(self):
        return self.status_text


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


class Api11PathsResponse(AbstractBaseHttpResponse, JsonResponseMixin):
    """
    This class models a response from any of the endpoints in most of 11Paths APIs.

    It consists of a "data" and an "error" elements. Although normally only one of them will be present, they are not
    mutually exclusive, since errors can be non fatal, and therefore a response could have valid information in the data
    field and at the same time inform of an error.
    """
    def __init__(self, resp):
        super(Api11PathsResponse, self).__init__(resp)
        self._body = self.urllib3_response.data

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
