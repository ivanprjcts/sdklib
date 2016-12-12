=============
Release Notes
=============

---

Upgrading
=========

To upgrade Sdklib to the latest version, use pip:
::
    pip install -U sdklib


Sdklib 1.4.1
============

- Fix bug: ensure url path params is never None.


Sdklib 1.4
==========

- Add XMLRenderer interface.
- Add json property to response.
- Add logger.
- Allow to replace content-type header value.


Sdklib 1.3
==========

- Add timeout decorator.
- Add generate_url_path function.
- Add new url parameters.
- Add get, post, put, patch and delete methods.
- Add XML response parser.
- Generate docs with sphinx.


Sdklib 1.2
==========

- Add incognito mode.


Sdklib 1.1
==========

- By default, no Content-type header in requests without body or files.
- Add file attribute to sdk response.
- Allow multipart body with custom content-type in data forms.
- Allow to add custom response_class.


Sdklib 1.0
==========

- Use urllib3.


Sdklib 0.5.2.1
==============

- Bug fixing.


Sdklib 0.5.2
============

- Bug fixing.
- Allow passing files and form_parameters as tuples when request is encoded multipart


Sdklib 0.5.1
============

- Bug fixing.


Sdklib 0.5
==========

- Add new parse as tuple list function.
- Add files parameter to http method.
- Infer content type header in all requests.


Sdklib 0.4.1
============

- Add parameters to strf timetizer functions.


Sdklib 0.4
==========

- Add file functions.
- Add parse as tuple list function.


Sdklib 0.3
==========

- Initial version.


