import unittest

from unittest.mock import patch
from HuetonApi.LightsApi import LightsApi, LightError, LightState, LightStateCommand
from test.MockResponse import MockResponse


@patch('HuetonApi.HueApi.requests')
class MyTestCase(unittest.TestCase):
    def setUp(self):
        lights_api = LightsApi()
        lights_api.init('newdeveloper')

        self.api = lights_api

    def test_get_all_lights(self, mock_requests):
        mock_requests.get.return_value = MockResponse(text='''{
        "1": { "name": "Bedroom"},
        "2": { "name": "Kitchen"}
        }''')

        lights = self.api.get_all_lights()

        self.assertEqual(2, len(lights))

    def test_get_new_lights(self, mock_requests):
        mock_requests.get.return_value = MockResponse(text='''{
        "7": {"name": "Hue Lamp 7"},
        "8": {"name": "Hue Lamp 8"},
        "lastscan": "2012-10-29T12:00:00"
        }''')

        scan = self.api.get_new_lights()

        self.assertEqual(2, len(scan.lights))
        self.assertEqual('2012-10-29T12:00:00', scan.lastscan)

    def test_search(self, mock_requests):
        mock_requests.post.return_value = MockResponse(text='''
        [ { "success": { "/lights": "Searching for new devices" } } ]
        ''')

        response = self.api.search_for_new_lights()

        self.assertEqual("Searching for new devices", response)

    def test_search_error(self, mock_requests):
        mock_requests.post.return_value = MockResponse(text='''
        [ { "error": { "/lights": "Searching for new devices" } } ]
        ''')

        self.assertRaisesRegexp(LightError, ".*Searching for new devices.*", self.api.search_for_new_lights)

    def test_get_light_attribute_and_state(self, mock_requests):
        mock_requests.get.return_value = MockResponse(text='''
        {
            "state": {
                "hue": 50000,
                "on": true,
                "effect": "none",
                "alert": "none",
                "bri": 200,
                "sat": 200,
                "ct": 500,
                "xy": [0.5, 0.5],
                "reachable": true,
                "colormode": "hs"
            },
            "type": "Living Colors",
            "name": "LC 1",
            "modelid": "LC0015",
            "swversion": "1.0.3",
            "pointsymbol": {
                "1": "none",
                "2": "none",
                "3": "none",
                "4": "none",
                "5": "none",
                "6": "none",
                "7": "none",
                "8": "none"
            }
        }
        ''')

        light_state = self.api.get_light_attributes_and_state(1)

        self.assertEqual("Living Colors", light_state.type)
        self.assertEqual("LC 1", light_state.name)
        self.assertEqual("LC0015", light_state.modelid)

    def test_rename(self, mock_requests):
        mock_requests.put.return_value = MockResponse(text='''
        [{"success":{"/lights/1/name":"Bedroom Light"}}]
        ''')

        name = self.api.rename(1, "Bedroom Light")

        self.assertEqual("Bedroom Light", name)

    def test_set_light_state(self, mock_requests):
        mock_requests.put.return_value = MockResponse(text='''
        [
            {"success":{"/lights/1/state/bri":200}},
            {"success":{"/lights/1/state/on":true}},
            {"success":{"/lights/1/state/hue":50000}}
        ]
        ''')

        light_state = LightStateCommand(
            transitiontime=1
        )

        self.api.set_light_state(1, light_state)





if __name__ == '__main__':
    unittest.main()
