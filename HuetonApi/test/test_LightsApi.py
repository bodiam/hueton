import unittest
import HuetonApi.LightsApi

from unittest.mock import Mock
from HuetonApi.LightsApi import LightsApi


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # See http://stackoverflow.com/questions/11399148/how-to-mock-an-http-request-in-a-unit-testing-scenario-in-python
        mock = Mock()
        mock.return_value = "{}"

        self.mock_requests = mock
        self.old_requests = HuetonApi.HueApi.requests
        HuetonApi.HueApi.requests = self.mock_requests

    def tearDown(self):
        # It is very important that each unit test be isolated, so we need
        # to be good citizen and clean up after ourselves. This means that
        # we need to put back the correct `requests` module where it was
        HuetonApi.HueApi.requests.requests = self.old_requests

    def test_get_all_lights(self):
        api = LightsApi()
        api.init("newdeveloper")
        lights = api.get_all_lights()

        # self.mock_requests.get().return_value = '{"1": { "name": "Bedroom"},"2": { "name": "Kitchen"}}'

        url = "http://example.com"

        self.mock_requests.get.assert_called_with(url)

        self.assertEqual(3, len(lights))

        # def test_get_new_lights(self):
        #
        #
        # // given response
        # mock.response = {
        #     "7": {"name": "Hue Lamp 7"},
        #     "8": {"name": "Hue Lamp 8"},
        #     "lastscan": "2012-10-29T12:00:00"
        # }
        # // when calling get_all_lights
        # light_api.get_all_light
        #
        # // then
        # assert something


if __name__ == '__main__':
    unittest.main()
