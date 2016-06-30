# Renderers #

Renderers are the managers of request enconding.

Renderer name | Content-type | Encoding
--- | --- | ---
form | application/x-www-form-urlencoded | param1=value1&param2=value2
multpart | multipart/form-data | Content-Disposition: form-data; name="param1"\n\nvalue1
plain | text/plain; charset=utf-8 | param1=value1\nparam2=value2
json | application/json | {"param1": "value1", "param2": "value2"}

---

**Note**: The code is available in the [renderers.py](https://github.com/ivanprjcts/sdklib/tree/master/sdklib/http/renderers.py) module on GitHub.

---


## Render Objects


    class BaseRenderer():
    
        def encode_params(self, data=None, files=None, **kwargs):
            """
            Will successfully encode files when passed as a dict or a list of tuples. Order is retained if data 
            is a list of tuples but arbitrary if parameters are supplied as a dict.
            
            The tuples may be string (filepath), 2-tuples (filename, fileobj), 3-tuples (filename, fileobj, 
            contentype) or 4-tuples (filename, fileobj, contentype, custom_headers).
            """


## FormRenderer

Build the body for a `application/x-www-form-urlencoded` request.


## MultiPartRenderer

Build the body for a `multipart/form-data` request.


## PlainTextRenderer

Build the body for a `text/plain` request.


## JSONRenderer

Build the body for a `application/json` request.
