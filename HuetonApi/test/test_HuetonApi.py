#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_HuetonApi
------------

Tests for `HuetonApi` module.
"""

import unittest
from unittest.mock import patch
from test.MockResponse import MockResponse

from HuetonApi.HuetonApi import *


@patch('HuetonApi.HueApi.requests')
class TestHuetonApi(unittest.TestCase):
    def test_hello_world(self, mock_requests):
        self.assertEquals(4, 4)

    def test_register_new_developer(self, mock_requests):
        mock_requests.get.return_value = MockResponse(text='''
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
        api.init('newdeveloper')
        self.assertFalse(api.connect())

        mock_requests.post.return_value = MockResponse(text='''[{"devicetype":"test user","username":"newdeveloper"}]''')
        api.register()

        mock_requests.get.return_value = MockResponse(text='''[{"success":{"username": "1234567890"}}]''')
        self.assertTrue(api.connect())


if __name__ == '__main__':
    unittest.main()
