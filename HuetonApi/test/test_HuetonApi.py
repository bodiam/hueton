#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_HuetonApi
------------

Tests for `HuetonApi` module.
"""

import unittest
from unittest.mock import patch

from HuetonApi.HuetonApi import *


@patch('HuetonApi.HueApi.requests')
class TestHuetonapi(unittest.TestCase):
    def test_hello_world(self, mock_requests):
        self.assertEquals(4, 4)

    def test_register_new_developer(self, mock_requests):
        mock_requests.get.return_value = Response(text='''
        [
            {
                "error": {
                    "type": "1",
                    "address": "/",
                    "description":"unauthorized user"
                }
            }
        ]
        ''')

        api = HuetonApi()
        api.init('username')
        self.assertFalse(api.connect())

        mock_requests.get.return_value = Response(text='''[{"success":{"username": "1234567890"}}]''')
        api.register()

        self.assertTrue(api.connect())


class Response:
    def __init__(self, text):
        self.text = text


if __name__ == '__main__':
    unittest.main()
