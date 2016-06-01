# Renderers

## Introduction

Renderers are the managers of request enconding.

---

**Note**: The code is available in the [renderers.py](https://github.com/ivanprjcts/sdklib/blob/v1.0/sdklib/http/renderers.py) module on GitHub.

---


## Render class

Will successfully encode files when passed as a dict or a list of tuples. Order is retained if data is a list of tuples 
but arbitrary if parameters are supplied as a dict.

The tuples may be string (filepath), 2-tuples (filename, fileobj), 3-tuples (filename, fileobj, contentype) or 4-tuples 
(filename, fileobj, contentype, custom_headers).


```python
def encode_params(self, data=None, files=None, **kwargs):
```


## FormRender

Build the body for a `application/x-www-form-urlencoded` request.


## MultiPartRender

Build the body for a `multipart/form-data` request.


## PlainTextRender

Build the body for a `text/plain` request.


## JSONRender

Build the body for a `application/json` request.
