import unittest

from HuetonApi.GroupsApi import GroupsApi, Group

# Test for GroupsApi Class
class TestGroupsApi(unittest.TestCase):
    def test_addGroup(self):
        gApi = GroupsApi()
        group = Group("Test Group")
        gApi.addGroup(group)

        self.assertEqual(1, len(gApi.groups))

    def test_removeGroup(self):
        gApi = GroupsApi()
        group1 = Group("Test Group 1")
        group2 = Group("Test Group 2")

        gApi.addGroup(group1)
        gApi.addGroup(group2)

        self.assertEqual(2, len(gApi.groups))

        gApi.removeGroup(group2)

        self.assertEqual(1, len(gApi.groups))

    def test_addLightToGroup(self):
        gApi = GroupsApi()
        group1 = Group("Test Group 1")
        gApi.addGroup(group1)

        light = "will be a light"
        gApi.addLightToGroup(group1, light)

    def test_removeLightFromGroup(self):
        gApi = GroupsApi()
        group1 = Group("Test Group 1")
        gApi.addGroup(group1)

        light1 = "will be a light 1"
        light2 = "will be a light 2"
        gApi.addLightToGroup(group1, light1)
        gApi.addLightToGroup(group1, light2)

        self.assertEqual(2, gApi.getTotalLightsForGroup(group1))

        gApi.get_all_groups()

        gApi.removeLightFromGroup(group1, light2)

        self.assertEqual(1, gApi.getTotalLightsForGroup(group1))

        gApi.get_all_groups()

    def test_get_all_Groups(self):
        gApi = GroupsApi()

        group1 = Group("Group1")
        group2 = Group("Group2")
        group3 = Group("Group3")

        gApi.addGroup(group1)
        gApi.addGroup(group2)
        gApi.addGroup(group3)

        total = gApi.get_all_groups()

        self.assertEqual(3, total)


if __name__ == '__main__':
    unittest.main()
