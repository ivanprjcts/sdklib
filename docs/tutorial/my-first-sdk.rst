======================
Writing your First SDK
======================

Introduction
============

This tutorial will cover creating a simple SDK for managing a REST-ful API.

**Note**: The code for this tutorial is available in the `ivanprjcts/my-first-sdk <https://github.com/ivanprjcts/my-first-sdk>`_ repository on GitHub.


Setting up a new environment
============================

Before we do anything else we'll create a new virtual environment, using `virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.
This will make sure our package configuration is kept nicely isolated from any other projects we're working on.
::
    virtualenv env
    source env/bin/activate

Now that we're inside a virtualenv environment, we can install our package requirements.
::
    pip install sdklib

**Note:** To exit the virtualenv environment at any time, just type `deactivate`.

Getting started
===============

Okay, we're ready to get coding.
To get started, let's create a new project to work with.
::
    cd ~
    mkdir my-first-sdk
    cd my-first-sdk

Once that's done we can create project structure that we'll use to create a simple Web API Client SDK.
::
    mkdir first_sdk tests
    touch README.md first_sdk/__init__.py first_sdk/first_sdk.py tests/__init__.py tests/test_first_sdk.py
    tree
    .
    ├── README.md
    ├── first_sdk
    │   ├── __init__.py
    │   └── first_sdk.py
    └── tests
        ├── __init__.py
        └── test_first_sdk.py


My First SDK
============

We'll need to edit our `first_sdk/first_sdk.py` file:
::
    from sdklib.http import HttpSdk
    from sdklib.util.parser import safe_add_end_slash, parse_args


    class FirstSdk(HttpSdk):
        """
        My First Sdk.
        """
        DEFAULT_HOST = "http://mockapi.sdklib.org"

        API_ITEMS_URL_PATH = "/items/"

        def create_item(self, name, description=None):
            """
            Create an item.
            :param name: str
            :param description: str (optional)
            :return: SdkResponse
            """
            params = parse_args(name=name, description=description)
            return self.post(self.API_ITEMS_URL_PATH, body_params=params)

        def get_items(self, item_id=None):
            """
            Retrieve all items if 'item_id' is None. Otherwise, get specified item by 'item_id'.
            :param item_id: str (optional)
            :return: SdkResponse
            """
            return self.get(self.API_ITEMS_URL_PATH + safe_add_end_slash(item_id))

        def update_item(self, item_id, name, description=None):
            """
            Update an item.
            :param item_id: str
            :param name: str
            :param description: str (optional)
            :return: SdkResponse
            """
            params = parse_args(name=name, description=description)
            return self.put(self.API_ITEMS_URL_PATH + item_id + '/', body_params=params)

        def delete_item(self, item_id):
            """
            Remove an item.
            :param item_id: str
            :return: SdkResponse
            """
            return self.delete(self.API_ITEMS_URL_PATH + item_id + '/')


Okay, we're ready to test.


Testing my First SDK
====================

Let's edit our `tests/test_first_sdk.py` file:
::
    import unittest

    from first_sdk.first_sdk import FirstSdk


    class TestFirstSdk(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            cls.api = FirstSdk()

        @classmethod
        def tearDownClass(cls):
            pass

        def test_crud_items(self):
            """
            Test the creation, reading, update and deletion of an item.
            """
            response = self.api.create_item("ItemName", "Some description")
            self.assertEqual(response.status, 201)

            item_id = response.data["pk"]
            self.assertEqual("ItemName", response.data["name"])
            self.assertEqual("Some description", response.data["description"])

            response = self.api.get_items()
            self.assertEqual(response.status, 200)
            self.assertIn("results", response.data)
            self.assertTrue(isinstance(response.data["results"], list))

            response = self.api.get_items(item_id)
            self.assertEqual(response.status, 200)
            self.assertEqual("ItemName", response.data["name"])
            self.assertEqual("Some description", response.data["description"])

            response = self.api.update_item(item_id, "New name")
            self.assertEqual(response.status, 200)
            self.assertEqual("New name", response.data["name"])
            self.assertEqual("Some description", response.data["description"])

            response = self.api.delete_item(item_id)
            self.assertEqual(response.status, 204)

