from HuetonApi.HueApi import HueApi
import json


class LightsApi(HueApi):
    def init(self, developer_name):
        print("Hello %s" % developer_name)
        self.base_location = "http://192.168.2.196/api/"
        self.location = self.base_location + developer_name
        self.developer_name = developer_name

    def get_all_lights(self):
        """
        Gets a list of all lights that have been discovered by the bridge.
        """
        result = self.hue_get("/lights")
        parsed = json.loads(result)

        return [Light(id, parsed[id]["name"]) for id in parsed]

    def get_new_lights(self):
        """
        Gets a list of lights that were discovered the last time a search for new lights was performed.
        The list of new lights is always deleted when a new search is started.
        """
        result = self.hue_get("/lights/new")
        parsed = json.loads(result)

        scan = Scan(lastscan=parsed["lastscan"])
        parsed.pop("lastscan", None)

        scan.lights.extend([Light(id, parsed[id]["name"]) for id in parsed])
        return scan

    def search_for_new_lights(self):
        """
        Starts a search for new lights.

        Example: [ { "success": { "/lights": "Searching for new devices" } } ]
        """
        result = self.hue_post("/lights")
        parsed = json.loads(result)

        if "success" in parsed[0]:
            return parsed[0]["success"]["/lights"]
        else:
            raise SearchError("Error, invalid response: {}".format(result))


    def get_light_attributes_and_state(self, id):
        """
        Gets the attributes and state of a given light.

        Example:
        {
            "state": {
                "hue": 50000,
                "on": true,
                "effect": "none",
                "alert": "none",
                "bri": 200,
                "sat": 200,
                "ct": 500,
                "xy": [0.5, 0.5],
                "reachable": true,
                "colormode": "hs"
            },
            "type": "Living Colors",
            "name": "LC 1",
            "modelid": "LC0015",
            "swversion": "1.0.3",
            "pointsymbol": {
                "1": "none",
                "2": "none",
                "3": "none",
                "4": "none",
                "5": "none",
                "6": "none",
                "7": "none",
                "8": "none"
            }
        }
        """
        result = self.hue_get("/lights/" + str(id))
        parsed = json.loads(result)

        light_state = LightState()
        light_state.type = parsed["type"]
        light_state.name = parsed["name"]
        light_state.modelid = parsed["modelid"]
        light_state.swversion = parsed["swversion"]
        light_state.state = State()

        return light_state

    def rename(self, id, name):
        """
        Used to rename lights. A light can have its name changed when in any state, including when it is unreachable or off.

        If the name is already taken a space and number will be appended by the bridge e.g. ���Bedroom Light 1���.
        """
        pass

    def set_light_state(self, id):
        """
        Allows the user to turn the light on and off, modify the hue and effects.
        """
        pass


class Error(Exception):
    pass


class SearchError(Error):
    def __init__(self, message):
        self.message = message


class Scan:
    def __init__(self, lastscan):
        self.lastscan = lastscan
        self.lights = []


class Light:
    def __init__(self, id, name = None):
        self.id = id
        self.name = name


class LightState:
    state = type = name = modelid = swversion = pointsymbol = None


#     "type": "Living Colors",
# "name": "LC 1",
# "modelid": "LC0015",
# "swversion": "1.0.3",
# "pointsymbol": {
#     "1": "none",
#     "2": "none",
#     "3": "none",
#     "4": "none",
#     "5": "none",
#     "6": "none",
#     "7": "none",
#     "8": "none"
# }


class State:
    state = hue = effect = alert = bri = sat = ct = xy = reachable = colormode = None

#     "hue": 50000,
#     "on": true,
#     "effect": "none",
#     "alert": "none",
#     "bri": 200,
#     "sat": 200,
#     "ct": 500,
#     "xy": [0.5, 0.5],
#     "reachable": true,
#     "colormode": "hs"
#
#     def __init__(self):
#
