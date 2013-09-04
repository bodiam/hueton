from HuetonApi.HueApi import HueApi
import json
# Author: Enric Ballo
# GroupsApi Class


class GroupsApi():
    def __init__(self, developer_name, location):
        self.api = HueApi()
        self.api.init(developer_name, location)

    def get_all_groups(self):
        result = self.api.hue_get("/groups")
        parsed = json.loads(result)
        return [Group(id, parsed[id]["name"]) for id in parsed]

    def create_group(self):
        #check max=16
        pass

    def get_group_attributes(self):
        pass

    def set_group_attributes(self):
        pass

    def set_group_state(self):
        pass

    def delete_group(self):
        pass


# Group Class
class Group():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printDetails(self):
        print("ID : " + self.id)
        print("Name : " + self.name)