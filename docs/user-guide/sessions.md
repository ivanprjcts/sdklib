# Sessions

By default, all requests use cookies.

---

**Note**: The code is available in the [session.py](https://github.com/ivanprjcts/sdklib/tree/master/sdklib/http/session.py) module on GitHub.

---


## Cookie Object

The `Cookie` class implement the following methods:

* `.__init__(self, headers=None)`
* `.load_from_headers(self, headers)`
* `.as_cookie_header_value(self)`
* `.is_empty(self)`
* `.getcookie(self)`
* `.items(self)`
* `.get(self, key, default=None)`


Wrapper of python [cookie](https://docs.python.org/2/library/cookie.html) module.
