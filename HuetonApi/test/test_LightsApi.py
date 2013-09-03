import unittest

from HuetonApi.LightsApi import *


class MyTestCase(unittest.TestCase):
    def test_get_all_lights(self):
        api = LightsApi()
        api.init("newdeveloper")
        lights = api.get_all_lights()

        self.assertEqual(3, len(lights))

    def test_get_new_lights(self):

        // given response
        {
            "7": {"name": "Hue Lamp 7"},
            "8": {"name": "Hue Lamp 8"},
            "lastscan": "2012-10-29T12:00:00"
        }
        // when calling get_all_lights


        // then


if __name__ == '__main__':
    unittest.main()
