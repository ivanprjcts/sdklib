=============
Configuration
=============


DEFAULT_HOST
============
Default: "http://127.0.0.1:80"

A string that will be automatically included at the beginning of the url generated for doing each http request.

- It can be also modified by using set_default_host() class method.


DEFAULT_PROXY
=============
Default: None (no proxy)

A string that will be used to tell each request must be sent through this proxy server.
Use the scheme://hostname:port form.
If you need to use a proxy, you can configure individual requests with the *proxy* argument to any request method.

- It can be also modified by using set_default_proxy() class method.


DEFAULT_RENDERER
================
Default: JSONRenderer object

A renderer object that will be used to build the body for any request.

For more in depth information, see :ref:`renderers`.


URLS
====

prefix_url_path
~~~~~~~~~~~~~~~
Default: "" (Empty string)

A string that will be automatically included (prepended by default) to all urls.


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


response_class
==============
Default: HttpResponse


