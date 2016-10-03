.. _renderers:

=========
Renderers
=========

Renderers are the managers of request body enconding.


+-----------------+-------------------------------------+----------------------------------------------------------+
| Renderer name   | Content-type                        | Encoding                                                 |
+=================+=====================================+==========================================================+
| form            | application/x-www-form-urlencoded   | param1=value1&param2=value2                              |
+-----------------+-------------------------------------+----------------------------------------------------------+
| multpart        | multipart/form-data                 | Content-Disposition: form-data; name="param1"\n\nvalue1  |
+-----------------+-------------------------------------+----------------------------------------------------------+
| plain           | text/plain; charset=utf-8           | param1=value1\\nparam2=value2                            |
+-----------------+-------------------------------------+----------------------------------------------------------+
| json            |  application/json                   | {"param1": "value1", "param2": "value2"}                 |
+-----------------+-------------------------------------+----------------------------------------------------------+




JSONRenderer
============

Build the body for a `application/json` request.


FormRenderer
============

Build the body for a `application/x-www-form-urlencoded` request.


MultiPartRenderer
=================


Build the body for a `multipart/form-data` request.


PlainTextRenderer
=================

Build the body for a `text/plain` request.



Renderers module
================

.. automodule:: sdklib.http.renderers
    :members:
    :undoc-members:
    :show-inheritance: