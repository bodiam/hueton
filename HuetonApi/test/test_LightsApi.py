import unittest

from HuetonApi.LightsApi import *


class MyTestCase(unittest.TestCase):
    def test_get_all_lights(self):
        api = LightsApi()
        api.init("newdeveloper")
        lights = api.get_all_lights()

        self.assertEqual(3, len(lights))


if __name__ == '__main__':
    unittest.main()
