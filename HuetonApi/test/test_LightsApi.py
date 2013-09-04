import unittest

from unittest.mock import patch
from HuetonApi.LightsApi import LightsApi, SearchError
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

        self.assertRaisesRegexp(SearchError, ".*Searching for new devices.*", self.api.search_for_new_lights)


if __name__ == '__main__':
    unittest.main()
