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


    def get_light_attributes_and_state(self):
        """
        Gets the attributes and state of a given light.
        """
        pass

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

    def add_light(self, light):
        self.lights.light


class Light:
    def __init__(self, light_id, name=""):
        self.id = light_id
        self.name = name

    def printDetails(self):
        print("Id :" + str(self.id))
        print("Name :" + self.name)

