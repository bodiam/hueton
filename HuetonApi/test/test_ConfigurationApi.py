import unittest

from unittest.mock import patch
from test.MockResponse import MockResponse
from HuetonApi.ConfigurationApi import ConfigurationApi, Configuration

# Test for GroupsApi Class
@patch('HuetonApi.HueApi.requests')
class TestConfigurationApi(unittest.TestCase):
    def setUp(self):
        developer = 'hueton'
        bridge = 'http://192.168.2.196/api/'
        groups_api = ConfigurationApi(developer, bridge)
        self.api = groups_api

    def test_get_configuration(self, mock_requests):
        mock_requests.get.return_value = MockResponse(text='''{
    "proxyport": 0,
    "UTC": "2012-10-29T12:00:00",
    "name": "Smartbridge 1",
    "swupdate": {
        "updatestate":1,
         "url": "www.meethue.com/patchnotes/1453",
         "text": "This is a software update",
         "notify": false
     },
    "whitelist": {
        "1234567890": {
            "last use date": "2010-10-17T01:23:20",
            "create date": "2010-10-17T01:23:20",
            "name": "iPhone Web 1"
        }
    },
    "swversion": "01003542",
    "proxyaddress": "none",
    "mac": "00:17:88:00:00:00",
    "linkbutton": false,
    "ipaddress": "192.168.1.100",
    "netmask": "255.255.0.0",
    "gateway": "192.168.0.1",
    "dhcp": false
}
''')

        configuration = self.api.get_configuration()

        self.assertEqual(0, configuration.proxyport)
        self.assertEqual("2012-10-29T12:00:00", configuration.UTC)
        self.assertEqual("Smartbridge 1", configuration.name)
        self.assertEqual("2010-10-17T01:23:20", configuration.whitelist['1234567890']["last use date"])

    def test_modify_configuration(self, mock_requests):
        mock_requests.put.return_value = MockResponse(text='''{
    "name": "Updated"
}''')

        configuration = Configuration(name="Test 123")

        result = self.api.modify_configuration(configuration)

        self.assertEqual("Updated", result.name)



