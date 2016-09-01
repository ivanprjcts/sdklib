=================================
Sdklib: the client side framework
=================================

|Build Status| |Codecov Status| |Pypi Version| |Code Climate| |Requirements Status|

Sdklib helps you to write you own client library which will consume a specific service.

.. |Build Status| image:: https://travis-ci.org/ivanprjcts/sdklib.svg?branch=master
   :target: https://travis-ci.org/ivanprjcts/sdklib
.. |Codecov Status| image:: https://img.shields.io/codecov/c/github/ivanprjcts/sdklib/master.svg
   :target: http://codecov.io/github/ivanprjcts/sdklib?branch=master
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

Install the `sdklib` package using pip.
::
    pip install sdklib


Usage
=====

My First SDK example.
::
    from sdklib.http import HttpSdk
    from sdklib.util.parser import safe_add_end_slash, parse_args
    
    
    class FirstSdk(HttpSdk):
        """
        My First Sdk.
        """
        DEFAULT_HOST = "http://api.spring16.equinox.local"
        
        API_ITEMS_URL_PATH = "/api/1.0/items/"
         
        def create_item(self, name, description=None):
            """
            Create an item.
            :param name: str
            :param description: str (optional)
            :return: SdkResponse
            """
            params = parse_args(name=name, description=description)
            return self._http_request("POST", self.API_ITEMS_URL_PATH, body_params=params)
    
        def get_items(self, item_id=None):
            """
            Retrieve all items if 'item_id' is None. Otherwise, get specified item by 'item_id'.
            :param item_id: str (optional)
            :return: SdkResponse
            """
            return self._http_request("GET", self.API_ITEMS_URL_PATH + safe_add_end_slash(item_id))
    
        def update_item(self, item_id, name, description=None):
            """
            Update an item.
            :param item_id: str
            :param name: str
            :param description: str (optional)
            :return: SdkResponse
            """
            params = parse_args(name=name, description=description)
            return self._http_request("PUT", self.API_ITEMS_URL_PATH + item_id + '/', body_params=params)

        def delete_item(self, item_id):
            """
            Remove an item.
            :param item_id: str
            :return: SdkResponse
            """
            return self._http_request("DELETE", self.API_ITEMS_URL_PATH + item_id + '/')



Run the tests
=============

Change to 'project_directory' and then, run unittest from command line.
::
    cd project_directory/
    python -m unittest discover



Contributing
============

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the repository on GitHub to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published. Make sure to add yourself to Authors.


Authors
=======

- Ivan Martin Vedriel - `@ivanprjcts <https://github.com/ivanprjcts>`_ - also maintainer.

