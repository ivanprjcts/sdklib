import base64
import hmac
import binascii

from hashlib import sha1

from sdklib.util.times import get_current_utc
from sdklib.http import url_encode
from sdklib.util.urls import ensure_url_path_starts_with_slash
from sdklib.util.structures import to_key_val_list
from sdklib.http.headers import AUTHORIZATION_HEADER_NAME, X_11PATHS_DATE_HEADER_NAME


X_11PATHS_HEADER_PREFIX = "X-11paths-"
X_11PATHS_HEADER_SEPARATOR = ":"
AUTHORIZATION_HEADER_FIELD_SEPARATOR = " "
AUTHORIZATION_METHOD = "11PATHS"


def basic_authentication(username, password):
    combined_username_password = username + b":" + password
    b64_combined = base64.b64encode(combined_username_password)
    return b"Basic " + b64_combined


def x_11paths_authentication(app_id, secret, context, utc=None):
    """
    Calculate the authentication headers to be sent with a request to the API
    :param app_id:
    :param secret:
    :param context
    :param utc:
    :return: array a map with the Authorization and Date headers needed to sign a Latch API request
    """
    if utc is None:
        utc = get_current_utc()
        utc = utc.strip()

    url_path = ensure_url_path_starts_with_slash(context.url_path)
    url_path_query = url_path
    if context.query_params is not None:
        url_path_query += "?%s" % (url_encode(context.query_params))

    string_to_sign = (context.method.upper().strip() + "\n" +
                      utc + "\n" +
                      _get_11paths_serialized_headers(context.headers) + "\n" +
                      url_path_query.strip())

    if context.body_params is not None:
        string_to_sign = string_to_sign + "\n" + url_encode(context.body_params, sort=True)

    authorization_header_value = (AUTHORIZATION_METHOD + AUTHORIZATION_HEADER_FIELD_SEPARATOR + app_id +
                                  AUTHORIZATION_HEADER_FIELD_SEPARATOR + _sign_data(secret, string_to_sign))

    return authorization_header_value, utc


def _sign_data(secret, data):
    """
    :param data: the string to sign
    :return: string base64 encoding of the HMAC-SHA1 hash of the data parameter using {@code secretKey} as cipher key.
    """
    sha1_hash = hmac.new(secret.encode(), data.encode(), sha1)
    return binascii.b2a_base64(sha1_hash.digest())[:-1].decode('utf8')


def _get_11paths_serialized_headers(x_headers):
    """
    Prepares and returns a string ready to be signed from the 11-paths specific HTTP headers received
    :param x_headers: a non necessarily ordered map (array without duplicates) of the HTTP headers to be ordered.
    :return: string The serialized headers, an empty string if no headers are passed, or None if there's a problem such
    as non 11paths specific headers
    """
    if x_headers:
        headers = to_key_val_list(x_headers, sort=True)
        serialized_headers = ""
        for key, value in headers:
            if not key.lower().startswith(X_11PATHS_HEADER_PREFIX.lower()):
                continue
            serialized_headers += key + X_11PATHS_HEADER_SEPARATOR + value + " "
        return serialized_headers.strip()
    else:
        return ""


class AbstractAuthentication(object):

    def apply_authentication(self, context):
        return context


class X11PathsAuthentication(AbstractAuthentication):

    def __init__(self, app_id, secret, utc=None):
        self.app_id = app_id
        self.secret = secret
        self.utc = utc

    def apply_authentication(self, context):
        authorization_value, utc_value = x_11paths_authentication(self.app_id, self.secret, context, utc=self.utc)
        context.headers[AUTHORIZATION_HEADER_NAME] = authorization_value
        context.headers[X_11PATHS_DATE_HEADER_NAME] = utc_value
        return context


class BasicAuthentication(AbstractAuthentication):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def apply_authentication(self, context):
        context.headers[AUTHORIZATION_HEADER_NAME] = basic_authentication(self.username, self.password)
        return context
