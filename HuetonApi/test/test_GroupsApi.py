import unittest

from unittest.mock import patch
from HuetonApi.GroupsApi import GroupsApi, Action
from test.MockResponse import MockResponse

# Test for GroupsApi Class
@patch('HuetonApi.HueApi.requests')
class TestGroupsApi(unittest.TestCase):
    def setUp(self):
        developer = 'hueton'
        bridge = 'http://192.168.2.196/api/'
        groups_api = GroupsApi(developer, bridge)
        self.api = groups_api

    def test_get_all_groups(self, mock_requests):
        mock_requests.get.return_value = MockResponse(text='''{
        "1": { "name": "Group 1" },
        "2": { "name": "VRC 2" }
        }''')

        groups = self.api.get_all_groups()

        self.assertEqual(2, len(groups))

#    def test_create_group(self):

    def test_get_group_attributes(self, mock_requests):
        mock_requests.get.return_value = MockResponse(text='''{
        "action": { "on": true,
                    "hue": 0,
                    "effect": "none",
                    "bri": 100,
                    "sat": 100,
                    "ct": 500,
                    "xy": [0.5, 0.5]
                  },
        "lights": [ "1","2" ],
        "name": "bedroom",
        "scenes": {     }
        }''')

        group = self.api.get_group_attributes(1)

        self.assertEqual(group.id, 1)
        self.assertEqual(group.name, "bedroom")

    def test_set_group_attributes(self, mock_requests):
        mock_requests.put.return_value = MockResponse(text='''
        [ {"success":{"/groups/1/lights":["1"]}},
          {"success":{"/groups/1/name":"test_group"}}]''')

        group_id = 1
        group_name = 'test_group'
        lights_id = ['1']

        result = self.api.set_group_attributes(group_id, group_name, lights_id)

        self.assertEqual("success", result)

    def test_set_group_state(self, mock_requests):
        mock_requests.put.return_value = MockResponse(text='''
        [ {"success":{"/groups/1/action/on": true}},
          {"success":{"/groups/1/action/effect":"colorloop"}},
          {"success":{"/groups/1/action/hue":6000}}]''')

        group_id = 1
        action = Action(True, 6000)
        effect = 'colorloop'
        result = self.api.set_group_state(group_id, action, effect)

        self.assertEqual("success", result)

#    def test_delete_group(self):


if __name__ == '__main__':
    unittest.main()
