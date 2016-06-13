import base64
import logging
import hmac
import binascii

from hashlib import sha1

from sdklib.util.times import get_current_utc
from sdklib.http import url_encode


X_11PATHS_HEADER_PREFIX = "X-11paths-"
X_11PATHS_HEADER_SEPARATOR = ":"
AUTHORIZATION_HEADER_FIELD_SEPARATOR = " "
AUTHORIZATION_METHOD = "11PATHS"


def basic_authentication(username, password):
    combined_username_password = "%s:%s" % (username, password)
    b64_combined = base64.b64encode(combined_username_password)
    return "Basic %s" % b64_combined


def x_11paths_authentication(app_id, secret, http_method, url_path_query, x_headers=None, params=None, utc=None):
    """
    Calculate the authentication headers to be sent with a request to the API
    :param app_id:
    :param secret:
    :param http_method: the HTTP Method, currently only GET is supported
    :param url_path_query: the urlencoded string including the path (from the first forward slash) and the parameters
    :param x_headers: HTTP headers specific to the 11-paths API. null if not needed.
    :param params:
    :param utc:
    :return: array a map with the Authorization and Date headers needed to sign a Latch API request
    """
    if utc is None:
        utc = get_current_utc()
        utc = utc.strip()

    string_to_sign = (http_method.upper().strip() + "\n" +
                      utc + "\n" +
                      _get_serialized_headers(x_headers) + "\n" +
                      url_path_query.strip())

    if params is not None:
        string_to_sign = string_to_sign + "\n" + url_encode(params, sort=True)

    authorization_header = (AUTHORIZATION_METHOD + AUTHORIZATION_HEADER_FIELD_SEPARATOR + app_id +
                            AUTHORIZATION_HEADER_FIELD_SEPARATOR + _sign_data(secret, string_to_sign))

    return authorization_header, utc


def _sign_data(secret, data):
    """
    :param data: the string to sign
    :return: string base64 encoding of the HMAC-SHA1 hash of the data parameter using {@code secretKey} as cipher key.
    """
    sha1_hash = hmac.new(secret.encode(), data.encode(), sha1)
    return binascii.b2a_base64(sha1_hash.digest())[:-1].decode('utf8')


def _get_serialized_headers(x_headers):
    """
    Prepares and returns a string ready to be signed from the 11-paths specific HTTP headers received
    :param x_headers: a non necessarily ordered map (array without duplicates) of the HTTP headers to be ordered.
    :return: string The serialized headers, an empty string if no headers are passed, or None if there's a problem such
    as non 11paths specific headers
    """
    if x_headers:
        headers = dict((k.lower(), v) for k, v in x_headers.iteritems())
        headers.sort()
        serialized_headers = ""
        for key, value in headers:
            if not key.startsWith(X_11PATHS_HEADER_PREFIX.lower()):
                logging.error(
                    "Error serializing headers. Only specific " + X_11PATHS_HEADER_PREFIX + " headers need to be singed")
                return None
            serialized_headers += key + X_11PATHS_HEADER_SEPARATOR + value + " "
        return serialized_headers.strip()
    else:
        return ""
