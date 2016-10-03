==============
Authentication
==============

Session authentication
======================

Session authentication is mostly used for AJAX clients that are running in the same session context as a website.

A client usually authenticates with its credentials and receives a session_id (which can be stored in a cookie) and attaches this to
every subsequent outgoing request. So this could be considered a "token" as it is the equivalent of a set of credentials.
It is just an identifier and the server does everything else.

HttpSdk class implements a mechanism to save automatically cookies embedded into *SET-COOKIE* header in each response.

If a cookie object is stored locally, then every request will contain a *COOKIE* header with this value.


Cookie Object
~~~~~~~~~~~~~

The `Cookie` class implement the following methods:

- `.__init__(self, headers=None)`
- `.load_from_headers(self, headers)`
- `.as_cookie_header_value(self)`
- `.is_empty(self)`
- `.getcookie(self)`
- `.items(self)`
- `.get(self, key, default=None)`


Wrapper of python `cookie <https://docs.python.org/2/library/cookie.html>`_ module.


Login method
~~~~~~~~~~~~
Sdklib provides an abstract method for login purposes.

- `.login(self, **kargs)`

Do a `POST` request to `LOGIN_URL_PATH` using parameters passed to method.


CRSR Token
~~~~~~~~~~

Sometimes, you'll need to make sure you include a valid CSRF token for any "unsafe" HTTP method calls, such as PUT,
PATCH, POST or DELETE requests.



Basic authentication
====================

HTTP Basic authentication (BA) implementation is the simplest technique for enforcing access controls to web resources
because it doesn't require cookies, session identifiers, or login pages; rather, HTTP Basic authentication uses standard
fields in the HTTP header, obviating the need for handshakes.

The Authorization header
~~~~~~~~~~~~~~~~~~~~~~~~
The Authorization field is constructed as follows:

1. The username and password are combined with a single colon.
2. The resulting string is encoded using the RFC2045-MIME variant of Base64, except not limited to 76 char/line.
3. The authorization method and a space i.e. "Basic " is then put before the encoded string.

For example,
::
    Authorization: Basic QWxhZGRpbjpPcGVuU2VzYW1l


11Paths authentication
======================

All requests must be signed. The signing process is a simplified version of the 2-legged Oauth protocol.

Every HTTP request to the API must be accompanied by two authentication headers: Authorization and Date.

The Authorization header
~~~~~~~~~~~~~~~~~~~~~~~~
The Authorization header must have the following format:
::
    11PATHS requestId requestSignature

- **requestId** is an alphanumeric identifier obtained when registering a new API.
- **11PATHS** is a constant that determines the Authentication method.
- **applicationId** is an alphanumeric identifier obtained when registering a new application.
- **requestSignature** is a signature derived from the url, parameters, custom headers and date of the current request, all hashed using a secret that is also obtained with the applicationId when registering the application.

The request signature is a base64 encoded and HMAC-SHA1 signed string. The string must be created following this process.

1. Start with an empty string.
2. Append the uppercase method name. Currently, only the values GET, POST, PUT, DELETE are supported.
3. Append a line separator, " " (unicode point U+000A).
4. Append a string with the current date in the exact format yyyy-MM-dd HH:mm:ss. Everything in the format should be self explanatory, noting that everything is numeric and should be zero-padded if needed so that all numbers have two digits except the year, having four. This value must be kept to be used in the Date header. The signature checking process will fail if both don't match.
5. Append a line separator, " " (unicode point U+000A).
6. Serialize all headers specific to this application (not every HTTP header in the request). These headers all have their names starting with X-11paths-.

    a. Convert all header names to lower case.
    b. Order the headers by header name in alphabetical ascending order.
    c. For every header value, convert multiline headers into single line by replacing newline characters " " by single spaces " ".
    d. Create an empty string. Then, for every header after the order and transformations above, add to the newly created string the header name followed by a colon ":" and followed by the header value. Each name:value should be separated from the next by a single space " ".
    e. Trim the string to make sure it doesn't contain any spacing characters at the beginning or end.
7. Append a line separator, " " (unicode point U+000A).
8. Append the url encoded query string consisting on the path (starting with the first forward slash) and the query parameters. The query string must not contain the host name or port, and must not contain any spacing characters prefixing or suffixing it.
9. Only for POST or PUT requests, attach a line separator, " " (Unicode Point U+000A).
10. Only for POST or PUT requests, serialize the request parameters as follows, the name of the parameter and its value, the UTF-8 representation of its URL coding.

    a. Order the parameters by parameter name in ascending alphabetical order and then by parameter value.
    b. Create an empty chain. Then, for each parameter after ordering, add to the newly created chain the parameter name followed by an equal sign "=" and the value of the parameter. Each name=value should be separated from the next by an ampersand "&".
    c. Trim the string to make sure it doesn't contain any spacing characters at the beginning or end.

Once the string has been created following the process described above, it must be signed using the HMAC-SHA1 algorithm and the secret that was obtained when registering the application. After signing, its raw binary data must be encoded in base64. The resulting string is the requestSignature to be added to Authorization header.

The X-11Paths-Date header
~~~~~~~~~~~~~~~~~~~~~~~~~
The **X-11Paths-Date** header contains the value of the current UTC date and must have the following format:
::
    yyyy-MM-dd HH:mm:ss

- **yyyy** is the year.
- **MM** is the number of month.
- **dd** is the number of day.
- **HH** is the hour in 24h format.
- **mm** is the minute within the hour and ss is the second within the minute.

All values must be zero-padded so that they are all 2 digit values except for the year which is 4.

It is very important that the value and format of this header is the exact same used in the process of creating the **requestSignature** for the authorization header as explained above.

Note you can still use the standard HTTP Header **Date** in whichever format you want, such as RFC 1123. Just make sure to not confuse both and always use the value you use in **X-11Paths-Date** in the signature process. The API will ignore the standard **Date** header.


OAuth 2.0
=========

Future work.