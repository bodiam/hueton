from HuetonApi.HueApi import HueApi
from HuetonApi.LightsApi import Light
import json
# Author: Enric Ballo
# GroupsApi Class


class GroupsApi():
    """
    Gets a list of all groups that have been added to the bridge.
    A group is a list of lights that can be created,
    modified and deleted by a user.
    The maximum numbers of groups is 16. N.B.
    For the first bridge firmware release,
    bridge software version 01003542 only, a
    limited number of these APIs are supported in
    the firmware so only control of groups/0 is
    supported.
    """
    def __init__(self, developer_name, location):
        self.api = HueApi()
        self.api.init(developer_name, location)

    def get_all_groups(self):
        """
        Returns a list of all groups in the system, each group has a name
        and unique identification number.
        """
        result = self.api.hue_get("/groups")
        parsed = json.loads(result)
        return [Group(id, parsed[id]["name"]) for id in parsed]

    def create_group(self):
        #check max=16
        #Not suported yet
        pass

    def get_group_attributes(self, group_id):
        """
        Gets the name, light membership and last command for a given group.
        """
        result = self.api.hue_get("/groups/" + str(group_id))
        parsed = json.loads(result)

        #Group Name
        group_name = parsed["name"]

        #Lights
        lights = []
        for light in parsed["lights"]:
            lights.append(Light(int(light)))

        #Scenes (NOT IMPLEMENTED)
        scenes = []
        for scene in parsed["scenes"]:
            scenes.append(Scene())

        #Last Actions
        action = parsed["action"]
        last_action = Action(action["on"], action["hue"], action["effect"], action["bri"], action["sat"], action["ct"], action["xy"])

        group = Group(group_id, group_name, lights, last_action, scenes)
        return group

    def set_group_attributes(self):
        pass

    def set_group_state(self):
        pass

    def delete_group(self):
        pass


# Group Class
class Group():
    def __init__(self, group_id, group_name, lights=[], last_action="", scenes=""):
        self.id = int(group_id)
        self.group_name = group_name
        self.lights = lights
        self.last_action = last_action
        self.scenes = scenes

    def print_details(self):
        print("Id : " + str(self.id))
        print("Name : " + self.group_name)
        print("== Last Action :")
        print(self.last_action.print_details())
        print("== Lights Details")
        for light in self.lights:
            print(light.print_details())
        print("== Scenes Details")
        for scene in self.scenes:
            print(scene.print_details())


class Scene():
    def __init__(self):
        pass

    def print_details(self):
        print("Scenes not implemented")


class Action():
    def __init__(self, on, hue, effect, bri, sat, ct, xy):
        self.on = on
        self.hue = hue
        self.effect = effect
        self.bri = bri
        self.sat = sat
        self.ct = ct
        self.xy = xy

    def print_details(self):
        print("on :" + str(self.on))
        print("hue :" + str(self.hue))
        print("effect :" + self.effect)
        print("bri :" + str(self.bri))
        print("sat :" + str(self.sat))
        print("ct :" + str(self.ct))
        print("xy :")
        print(self.xy)
