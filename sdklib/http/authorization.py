# -*- coding: utf-8 -*-

import base64
import hmac
import binascii

from hashlib import sha1

from sdklib.compat import convert_str_to_bytes, convert_bytes_to_str
from sdklib.http import url_encode
from sdklib.http.renderers import FormRenderer, guess_file_name_stream_type_header
from sdklib.http.headers import (
    AUTHORIZATION_HEADER_NAME, X_11PATHS_DATE_HEADER_NAME, X_11PATHS_BODY_HASH_HEADER_NAME,
    X_11PATHS_FILE_HASH_HEADER_NAME
)
from sdklib.util.times import get_current_utc
from sdklib.util.urls import ensure_url_path_starts_with_slash
from sdklib.util.structures import to_key_val_list
from sdklib.http.methods import PUT_METHOD, POST_METHOD
from sdklib.http.headers import CONTENT_TYPE_HEADER_NAME


X_11PATHS_HEADER_PREFIX = "X-11paths-"
X_11PATHS_HEADER_SEPARATOR = ":"
AUTHORIZATION_HEADER_FIELD_SEPARATOR = " "
AUTHORIZATION_METHOD = "11PATHS"


def basic_authorization(username, password):
    combined_username_password = username + ":" + password
    b64_combined = base64.b64encode(convert_str_to_bytes(combined_username_password))
    return "Basic " + convert_bytes_to_str(b64_combined)


def x_11paths_authorization(app_id, secret, context, utc=None):
    """
    Calculate the authentication headers to be sent with a request to the API.

    :param app_id:
    :param secret:
    :param context
    :param utc:
    :return: array a map with the Authorization and Date headers needed to sign a Latch API request
    """
    utc = utc or context.headers[X_11PATHS_DATE_HEADER_NAME]

    url_path = ensure_url_path_starts_with_slash(context.url_path)
    url_path_query = url_path
    if context.query_params:
        url_path_query += "?%s" % (url_encode(context.query_params, sort=True))

    string_to_sign = (context.method.upper().strip() + "\n" +
                      utc + "\n" +
                      _get_11paths_serialized_headers(context.headers) + "\n" +
                      url_path_query.strip())

    if context.body_params and isinstance(context.renderer, FormRenderer):
        string_to_sign = string_to_sign + "\n" + url_encode(context.body_params, sort=True).replace("&", "")

    authorization_header_value = (AUTHORIZATION_METHOD + AUTHORIZATION_HEADER_FIELD_SEPARATOR + app_id +
                                  AUTHORIZATION_HEADER_FIELD_SEPARATOR + _sign_data(secret, string_to_sign))

    return authorization_header_value


def _sign_data(secret, data):
    """
    Sign data.

    :param data: the string to sign
    :return: string base64 encoding of the HMAC-SHA1 hash of the data parameter using {@code secretKey} as cipher key.
    """
    sha1_hash = hmac.new(secret.encode(), data.encode(), sha1)
    return binascii.b2a_base64(sha1_hash.digest())[:-1].decode('utf8')


def _hash_body(context):
    body, _ = context.renderer.encode_params(context.body_params, files=context.files)
    return sha1(convert_str_to_bytes(body)).hexdigest()


def _hash_file(context):
    files = context.files
    assert len(files) == 1, "This method only can sign requests with one file"

    for param in files:
        _, fdata, _, _ = guess_file_name_stream_type_header(files[param])
        return sha1(convert_str_to_bytes(fdata)).hexdigest()


def _get_utc():
    utc = get_current_utc()
    return utc.strip()


def _get_11paths_serialized_headers(x_headers):
    """
    Prepares and returns a string ready to be signed from the 11-paths specific HTTP headers received.

    :param x_headers: a non necessarily ordered map (array without duplicates) of the HTTP headers to be ordered.
    :return: string The serialized headers, an empty string if no headers are passed, or None if there's a problem such
    as non 11paths specific headers
    """
    if x_headers:
        headers = to_key_val_list(x_headers, sort=True, insensitive=True)
        serialized_headers = ""
        for key, value in headers:
            if key.lower().startswith(X_11PATHS_HEADER_PREFIX.lower()) and \
                            key.lower() != X_11PATHS_DATE_HEADER_NAME.lower():
                serialized_headers += key.lower() + X_11PATHS_HEADER_SEPARATOR + value.replace("\n", " ") + " "
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
        context.headers[X_11PATHS_DATE_HEADER_NAME] = self.utc or _get_utc()
        if context.method == POST_METHOD or context.method == PUT_METHOD:
            if CONTENT_TYPE_HEADER_NAME in context.headers and \
                    context.headers[CONTENT_TYPE_HEADER_NAME].lower().startswith("multipart/form-data"):
                context.headers[X_11PATHS_FILE_HASH_HEADER_NAME] = _hash_file(context)
            elif CONTENT_TYPE_HEADER_NAME in context.headers and \
                    context.headers[CONTENT_TYPE_HEADER_NAME].lower() == "application/json":
                context.headers[X_11PATHS_BODY_HASH_HEADER_NAME] = _hash_body(context)
            elif CONTENT_TYPE_HEADER_NAME not in context.headers and not context.body_params:
                # 11paths bug: server validate that content-type header exists in POST and PUT requests
                context.headers[CONTENT_TYPE_HEADER_NAME] = "application/x-www-form-urlencoded"
        context.headers[AUTHORIZATION_HEADER_NAME] = x_11paths_authorization(
            self.app_id,
            self.secret,
            context
        )
        return context


class BasicAuthentication(AbstractAuthentication):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def apply_authentication(self, context):
        context.headers[AUTHORIZATION_HEADER_NAME] = basic_authorization(self.username, self.password)
        return context
