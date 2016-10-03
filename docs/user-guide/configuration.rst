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


prefix_url_path
===============
Default: "" (Empty string)


url_path_params
===============
Default: {} (Empty dictionary)


url_path_format
===============
Default: None (null value)


authentication_instances
========================
Default: () (Empty tuple)


response_class
==============
Default: HttpResponse


