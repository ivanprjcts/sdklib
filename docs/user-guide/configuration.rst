=============
Configuration
=============


Secure HTTP
===========

By default, ssl certificates are not validated.


Default Configuration
=====================

+------------------+-------------------------------------+
| Parameter        | Default value                       |
+==================+=====================================+
| DEFAULT_HOST     | http://127.0.0.1:80                 |
+------------------+-------------------------------------+
| DEFAULT_PROXY    | None                                |
+------------------+-------------------------------------+
| DEFAULT_RENDERER | JSONRenderer()                      |
+------------------+-------------------------------------+


DEFAULT_HOST
~~~~~~~~~~~~
Value: "http://127.0.0.1:80"

A string that will be used as host default value.

- It can be also modified by using set_default_host() class method.


DEFAULT_PROXY
~~~~~~~~~~~~~
Value: None (no proxy)

A string that will be used as proxy default value.

- It can be also modified by using set_default_proxy() class method.


DEFAULT_RENDERER
~~~~~~~~~~~~~~~~
Value: JSONRenderer() object

A renderer object that will be used to build the body for any request.

For more in depth information, see :ref:`renderers`.


URLS
====

host
~~~~
Default: DEFAULT_HOST_

A string that will be automatically included at the beginning of the url generated for doing each http request.


prefix_url_path
~~~~~~~~~~~~~~~
Default: "" (Empty string)

A string that will be automatically prepended to all urls.


url_path_params
~~~~~~~~~~~~~~~
Default: {} (Empty dictionary)

A dictionary mapping strings to string format that take a model object and return the generated URL. It works like string format with dictionary:
::
    "/path/to/{project_id}/{lang}".format(**{"project_id": 1, "lang": "es"})

url_path_format
~~~~~~~~~~~~~~~
Default: None

A string that will be automatically included (suffixed) to all urls. For example:
::
    .json or .xml


authentication_instances
========================
Default: () (Empty tuple)

List (or tuple) of authentication objects that will be used for building the request.

For more in depth information, see :ref:`authentication`.


response_class
==============
Default: HttpResponse


For more in depth information, see :ref:`response`.

ssl_verify
==========
Default: None (undefined), validate certs (True)

Define if certificates are required for the SSL connection. They will be validated, and
if validation fails, the connection will also fail.

Values: (bool) `True` or `False

This value could also be defined using environment environment variable `SDKLIB_SSL_VERIFY`
::
    export SDKLIB_SSL_VERIFY=False
