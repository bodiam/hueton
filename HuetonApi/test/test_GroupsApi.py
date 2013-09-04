import unittest

from unittest.mock import patch
from HuetonApi.GroupsApi import GroupsApi
from test.Response import Response

# Test for GroupsApi Class


@patch('HuetonApi.HueApi.requests')
class TestGroupsApi(unittest.TestCase):
    def setUp(self):
        developer = 'newdeveloper'
        bridge = 'http://192.168.2.196/api/'
        groups_api = GroupsApi(developer, bridge)
        self.api = groups_api

    def test_get_all_groups(self, mock_requests):
        mock_requests.get.return_value = Response(text='''{
        "1": { "name": "Group 1" },
        "2": { "name": "VRC 2" }
        }''')

        groups = self.api.get_all_groups()

        self.assertEqual(2, len(groups))

#  def test_create_group(self):

#    def test_get_group_attributes(self):

#    def test_set_group_attributes(self):

#    def test_set_group_state(self):

#    def test_delete_group(self):


if __name__ == '__main__':
    unittest.main()
