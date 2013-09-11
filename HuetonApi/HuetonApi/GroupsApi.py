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

        return Group(group_id, group_name, lights, last_action, scenes)

    def set_group_attributes(self, group_id, group_name, lights_id):
        """
        Allows the user to modify the name and light membership of a group.

        group_name    string 0..32    The new name for the group.
                      If the name is already taken a space and number will
                      be appended by the bridge e.g. “Custom Group 1”. Optional
        lights_id    array of light IDs    The IDs of the lights that
                     should be in the group. This resource must contain an
                     array of at least one element.

        If an invalid light ID is given, error 7 will be returned and the
        group not created.
        """
        array_lights = '["' + '", "'.join(lights_id) + '"]'
        body = '{"name":"' + group_name + '","lights":' + array_lights + '}'

        result = self.api.hue_put("/groups/" + str(group_id), body)
        parsed = json.loads(result)

        if "success" in parsed[0]:
            return "success"
        else:
            raise GroupError("Error, invalid response: {}".format(result))

    def set_group_state(self):
        pass

    def delete_group(self):
        pass


# Group Class
class Group():
    def __init__(self, id, name, lights=[], last_action=None, scenes=None):
        self.id = id
        self.name = name
        self.lights = lights
        self.last_action = last_action
        self.scenes = scenes


class Scene():
    def __init__(self):
        pass


class Action():
    def __init__(self, on, hue, effect, bri, sat, ct, xy):
        self.on = on
        self.hue = hue
        self.effect = effect
        self.bri = bri
        self.sat = sat
        self.ct = ct
        self.xy = xy


class Error(Exception):
    pass


class GroupError(Error):
    def __init__(self, message):
        self.message = message
