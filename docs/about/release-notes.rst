=============
Release Notes
=============

Upgrading
=========

To upgrade Sdklib to the latest version, use pip:
::
    pip install -U sdklib


Sdklib 1.11.x series
===================

Sdklib 1.11.2
-------------

- Fix ssl_verify behaviour for old versions of urllib3.

Sdklib 1.11.1
-------------

- Fix 11paths authorization using body in python3.

Sdklib 1.11.0
-------------

- Allow ssl_verify config param.


Sdklib 1.10.x series
===================

Sdklib 1.10.5
-------------

- Fix multipart boundary characters according to RFC (https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html).

Sdklib 1.10.3
-------------

- New experimental feature: support socks proxy protocol.

Sdklib 1.10.2
-------------

- Fix bug.

Sdklib 1.10.1
-------------

- Improve getting text from lxml elements.

Sdklib 1.10.0
-------------

- Fix bug setting cookies after receiving several "Set-Cookie" headers.
- Update urllib3 version.
- Remove experimental support to proxy socks protocol.


Sdklib 1.9.x series
===================

Sdklib 1.9.6
------------

- Support proxy socks protocol.

Sdklib 1.9.5
------------

- Fix installation.

Sdklib 1.9.4
------------

- Move ignore warnings function to shortcuts.

Sdklib 1.9.3
------------

- Allow to ignore warnings.
- Fix bug in getparent htmlElem method.

Sdklib 1.9.2
------------

- Fix bug in HAR requests (urlencoded params were encoded twice).
- Add 'timeout' attribute to http_request_context.

Sdklib 1.9.1
------------

- Add getparent method to LxmlElem class.

Sdklib 1.9.0
------------

- Put 'incognito_mode' as class attribute.
- Add cache decorator for python 3+.


Sdklib 1.8.x series
===================

Sdklib 1.8.11
-------------

- Fix 11paths authorization bug in 'POST'/'PUT' json requests without body.
- Headers as case insensitive dictionary.

Sdklib 1.8.10
-------------

- Fix 11paths authorization bug in requests with query params.

Sdklib 1.8.9
------------

- Fix 11paths authorization bug in some 'POST', 'PUT' requests.

Sdklib 1.8.8
------------

- Create HTMLElem including AbstractBaseHTML functionality.
- Add HAR objects.
- Add cookie property to HttpRequestContext.
- Do not add *X_11PATHS_BODY_HASH* header when body is empty.
- Refactor HttpResponse.
- Add find_by_name method to html objects.

Sdklib 1.8.7
------------

- Update cookies rather than replace them.
- Fix "The HTTP reason phrase should not be" behave step.
- Add "The HTTP reason phrase should contain" behave step.
- Add BaseHttpResponse class.
- Fix some bugs (#50).

Sdklib 1.8.6
------------

- Fix 11paths authorization bug.
- Add insensitive (sort) parameter to to_key_val_list function.

Sdklib 1.8.5.3
--------------

- Fix behave steps bug.

Sdklib 1.8.5.2
--------------

- Fix Api11PathsResponse bug.

Sdklib 1.8.5.1
--------------

- Fix Api11PathsResponse bug.

Sdklib 1.8.5
------------

- Create AbstractHttpResponse class.
- Remove some properties from Api11PathsResponse.

Sdklib 1.8.4
------------

- Make get Api11PathsResponse data, error, code and message case insensitive.
- Add CaseInsensitiveDict class.
- Fix some bugs.

Sdklib 1.8.3
------------

- Add behave steps.
- Fix some bugs.
- Separate requirements_dev.txt into different files.

Sdklib 1.8.2
------------

- Add Api11PathsResponse.

Sdklib 1.8.1
------------

- Add guess_file_name_stream_type_header() method.
- Fix 11paths auth bug.

Sdklib 1.8
----------

- Add test coverage reports.
- Add some tests.
- Remove rrserver.
- Remove behave api steps.
- Remove unused modules.
- Fix some bugs.


Sdklib 1.7.x series
===================

Sdklib 1.7.2
------------

- Fix some bugs.

Sdklib 1.7.1
------------

- Fix some bugs.

Sdklib 1.7
----------

- Return more parameters into urlsplit function.
- Add generate_url() function.
- Add lxml as optional requirement.
- Support xpath functions such as contains() using lxml.


Sdklib 1.6.x series
===================

Sdklib 1.6.6
------------

- Allow to redirect http requests.

Sdklib 1.6.5
------------

- Use an internal logger instance to print request and response logs.
- Add clear method to http request context.
- Add fields_to_clear attribute to http request context.

Sdklib 1.6
----------

- Custom content-type header has priority over renderer content-type.
- Get update_content_type parameter from context.
- Add BaseRenderer.
- Add CustomRenderer.


Sdklib 1.5.x series
===================

Sdklib 1.5.2
------------

- Add manifest.

Sdklib 1.5.1
------------

- Fix requirements.

Sdklib 1.5
----------

- Add HTML parsed response.


Sdklib 1.4.x series
===================

Sdklib 1.4.2
------------

- Fix bug: 11paths authorization header is not correct using multiples form params.

Sdklib 1.4.1
------------

- Fix bug: ensure url path params is never None.

Sdklib 1.4
----------

- Add XMLRenderer interface.
- Add json property to response.
- Add logger.
- Allow to replace content-type header value.


Sdklib 1.3.x series
===================

- Add timeout decorator.
- Add generate_url_path function.
- Add new url parameters.
- Add get, post, put, patch and delete methods.
- Add XML response parser.
- Generate docs with sphinx.


Sdklib 1.2.x series
===================

- Add incognito mode.


Sdklib 1.1.x series
===================

- By default, no Content-type header in requests without body or files.
- Add file attribute to sdk response.
- Allow multipart body with custom content-type in data forms.
- Allow to add custom response_class.


Sdklib 1.0.x series
===================

Sdklib 1.0
----------

- Use urllib3.


Sdklib 0.x series
=================

Sdklib 0.5.2.1
--------------

- Bug fixing.

Sdklib 0.5.2
------------

- Bug fixing.
- Allow passing files and form_parameters as tuples when request is encoded multipart

Sdklib 0.5.1
------------

- Bug fixing.

Sdklib 0.5
----------

- Add new parse as tuple list function.
- Add files parameter to http method.
- Infer content type header in all requests.

Sdklib 0.4.1
------------

- Add parameters to strf timetizer functions.

Sdklib 0.4
----------

- Add file functions.
- Add parse as tuple list function.

Sdklib 0.3
----------

- Initial version.
