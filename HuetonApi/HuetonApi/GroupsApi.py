from HuetonApi.HueApi import HueApi
from HuetonApi.LightsApi import Light
import json
# Author: Enric Ballo
# GroupsApi Class


class GroupsApi(HueApi):
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
    def get_all_groups(self):
        """
        Returns a list of all groups in the system, each group has a name
        and unique identification number.
        """
        parsed = self.hue_get("/groups")
        return [Group(id, parsed[id]["name"]) for id in parsed]

    def create_group(self):
        #check max=16
        #Not suported yet
        pass

    def get_group_attributes(self, group_id):
        """
        Gets the name, light membership and last command for a given group.
        """
        parsed = self.hue_get("/groups/" + str(group_id))

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

        parsed = self.hue_put("/groups/" + str(group_id), body)

        if "success" in parsed[0]:
            return "success"
        else:
            raise GroupError("Error, invalid response: {}".format(result))

    def set_group_state(self, group_id, action=None, alert=None, effect=None, transition_time=None):
        """
        Modifies the state of all lights in a group.

        User created groups will have an ID of 1 or higher; 
        however a special group with an ID of 0 also exists 
        containing all the lamps known by the bridge.
        """
        properties = []

        if action is not None:
            if action.on is not None:
                on = ' "on" : ' + str(action.on)
                properties.append(on)
            if action.bri is not None:
                bri = ' "bri" : ' + action.bri
                properties.append(bri)
            if action.hue is not None:
                hue = ' "hue" : ' + str(action.hue)
                properties.append(hue)
            if action.sat is not None:
                sat = ' "sat" : ' + action.sat
                properties.append(sat)
            if action.xy is not None:
                xy = ' "xy" : ' + action.xy
                properties.append(xy)
            if action.ct is not None:
                ct = ' "ct" : ' + action.ct
                properties.append(ct)

        if alert is not None:
            alert = ' "alert" : ' + alert
            properties.append(alert)

        if effect is not None:
            effect = ' "effect" : ' + effect
            properties.append(effect)

        if transition_time is not None:
            transitiontime = ' "transitiontime" : ' + transition_time
            properties.append(transitiontime)

        # build the body message
        if len(properties) > 0:
            txt_body = ', '.join(properties)
            #print(txt_body)
            body = '{ ' + txt_body + '  }'

            parsed = self.hue_put("/groups/" + str(group_id) + '/action', body)

            if "success" in parsed[0]:
                return "success"
            else:
                raise GroupError("Error, invalid response: {}".format(result))
        else:
            raise GroupError("Error, no parameters found: ")

    def delete_group(self):
        """
        NOT SUPORTED
        """
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
    def __init__(self, on=None, hue=None, effect=None, bri=None, sat=None, ct=None, xy=None):
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
