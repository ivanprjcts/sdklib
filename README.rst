=================================
Sdklib: the client side framework
=================================

|Build Status| |Codecov Status| |Pypi Version| |Code Climate| |Requirements Status|

Sdklib helps you to write you own client library which will consume a specific service.

.. |Build Status| image:: https://travis-ci.org/ivanprjcts/sdklib.svg?branch=master
   :target: https://travis-ci.org/ivanprjcts/sdklib
.. |Codecov Status| image:: https://codecov.io/gh/ivanprjcts/sdklib/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ivanprjcts/sdklib
.. |Pypi Version| image:: https://img.shields.io/pypi/v/sdklib.svg
   :target: https://pypi.python.org/pypi/sdklib
.. |Code Climate| image:: https://codeclimate.com/github/ivanprjcts/sdklib/badges/gpa.svg
   :target: https://codeclimate.com/github/ivanprjcts/sdklib
.. |Requirements Status| image:: https://requires.io/github/ivanprjcts/sdklib/requirements.svg?branch=master
   :target: https://requires.io/github/ivanprjcts/sdklib/requirements/?branch=master


Highlights
==========

- Python 2.7+ or 3.3+.
- Only http/https protocol is currently supported.
- BDD integration.


Install
=======

Install the ``sdklib`` package using pip::

    pip install sdklib


Sample
======

Find my first SDK on github: https://github.com/ivanprjcts/my-first-sdk

.. code-block:: python

    from sdklib.http import HttpSdk

    class FirstSdk(HttpSdk):
        """
        My First Sdk.
        """
        DEFAULT_HOST = "http://mockapi.sdklib.org"

        API_ITEMS_URL_PATH = "/items/"

        def create_item(self, name, description=None):
            """
            Create an item.
            
            :type name: str
            :type description: str
            :return: SdkResponse
            """
            params = parse_args(name=name, description=description)
            return self.post(self.API_ITEMS_URL_PATH, body_params=params)


Run tests
=========

Running testing with coverage::

    py.test --cov=sdklib tests/


Contributing
============

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the repository on GitHub to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published. Make sure to add yourself to Authors.


Authors
=======

- Ivan Martin Vedriel - `@ivanprjcts <https://github.com/ivanprjcts>`_
- Rubén González Alonso - `@rgonalo <https://github.com/rgonalo>`_

