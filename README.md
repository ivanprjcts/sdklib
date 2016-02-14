SDK Helper Library
==================

- Make easier sdk libraries implementation.


## INSTALL

```
python setup.py install
```

## USAGE

```
from sdklib import SdkBase

class MySDK(SdkBase):
```


## Changelog

* Sdklib 0.3
    - Initial version.
    
* Sdklib 0.4
    - Add safe_add_end_slash function.
    - Add file functions.
    - Add parse as tuple list function.

* Sdklib 0.4.1
    - Add parameters to strf timetizer functions.
    
* Sdklib 0.5
    - Add new parse as tuple list function.
    - Add files parameter to http method.
    - Infer content type header in all requests.
    
* Sdklib 0.5.1
    - Bug fixing.

* Sdklib 0.5.2
    - Bug fixing.
    - Allow passing files and form_parameters as tuples when request is encoded multipart