# -*- coding: utf-8 -*-

import json
import logging
from xml.dom.minidom import parseString

from sdklib.compat import str
from sdklib.http.headers import CONTENT_TYPE_HEADER_NAME
from sdklib.http.renderers import JSONRenderer, XMLRenderer

logger = logging.getLogger(__name__)


def _get_pretty_body(headers, body):
    """
    Return a pretty printed body using the Content-Type header information.

    :param headers: Headers for the request/response (dict)
    :param body: Body to pretty print (string)
    :return: Body pretty printed (string)
    """
    try:
        if CONTENT_TYPE_HEADER_NAME in headers:
            if XMLRenderer.DEFAULT_CONTENT_TYPE == headers[CONTENT_TYPE_HEADER_NAME]:
                xml_parsed = parseString(body)
                pretty_xml_as_string = xml_parsed.toprettyxml()
                return pretty_xml_as_string
            elif JSONRenderer.DEFAULT_CONTENT_TYPE == headers[CONTENT_TYPE_HEADER_NAME]:
                decoded_body = body.decode('utf-8')
                parsed = json.loads(decoded_body)
                return json.dumps(parsed, sort_keys=True, indent=4)
    except:
        pass
    finally:
        return body


def log_print_request(method, url, query_params=None, headers=None, body=None):
    """
    Log an HTTP request data in a user-friendly representation.

    :param method: HTTP method
    :param url: URL
    :param query_params: Query parameters in the URL
    :param headers: Headers (dict)
    :param body: Body (raw body, string)
    :return: None
    """

    log_msg = '\n>>>>>>>>>>>>>>>>>>>>> Request >>>>>>>>>>>>>>>>>>> \n'
    log_msg += '\t> Method: %s\n' % method
    log_msg += '\t> Url: %s\n' % url
    if query_params is not None:
        log_msg += '\t> Query params: {}\n'.format(str(query_params))
    if headers is not None:
        log_msg += '\t> Headers:\n{}\n'.format(json.dumps(dict(headers), sort_keys=True, indent=4))
    if body is not None:
        try:
            log_msg += '\t> Payload sent:\n{}\n'.format(_get_pretty_body(headers, body))
        except:
            log_msg += "\t> Payload could't be formatted"

    logger.debug(log_msg)


def log_print_response(status_code, response, headers=None):
    """
    Log an HTTP response data in a user-friendly representation.

    :param status_code: HTTP Status Code
    :param response: Raw response content (string)
    :param headers: Headers in the response (dict)
    :return: None
    """

    log_msg = '\n<<<<<<<<<<<<<<<<<<<<<< Response <<<<<<<<<<<<<<<<<<\n'
    log_msg += '\t< Response code: {}\n'.format(str(status_code))
    if headers is not None:
        log_msg += '\t< Headers:\n{}\n'.format(json.dumps(dict(headers), sort_keys=True, indent=4))
    try:
        log_msg += '\t< Payload received:\n{}'.format(_get_pretty_body(headers, response))
    except:
        log_msg += '\t< Payload received:\n{}'.format(response)
    logger.debug(log_msg)
