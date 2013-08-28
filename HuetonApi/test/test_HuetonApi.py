#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_HuetonApi
------------

Tests for `HuetonApi` module.
"""

import os
import shutil
import unittest

from HuetonApi.HuetonApi import *


class TestHuetonapi(unittest.TestCase):
    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass

    def test_hello_world(self):
        print("hello")
        self.assertEquals(4, 4)

    def test_register_new_developer(self):
        api = HuetonApi()
        api.init('username')

        self.assertFalse(api.connect())

        api.register()

        self.assertTrue(api.connect())


if __name__ == '__main__':
    unittest.main()
