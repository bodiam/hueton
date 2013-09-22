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
            raise LightError("Error, invalid response: {}".format(result))

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

        light_state = LightState(
            type=parsed["type"],
            name=parsed["name"],
            model_id=parsed["modelid"],
            sw_version=parsed["swversion"],
            state=State()
        )

        return light_state

    def rename(self, id, name):
        """
        Used to rename lights. A light can have its name changed when in any state, including when it is unreachable or off.

        If the name is already taken a space and number will be appended by the bridge e.g. 'Bedroom Light 1'.

        Example:
        [{"success":{"/lights/1/name":"Bedroom Light"}}]
        """

        payload = json.dumps({"name": name})
        result = self.hue_put("/lights/{}".format(id), payload)
        parsed = json.loads(result)

        if "success" in parsed[0]:
            return parsed[0]["success"]["/lights/{}/name".format(id)]
        else:
            raise LightError("Error, invalid response: {}".format(result))

    def set_light_state(self, id, light_state):
        """
        Allows the user to turn the light on and off, modify the hue and effects.
        """

        input_map = vars(light_state)
        payload = dict((key, value) for key, value in input_map.items() if key not in ['self'] and value is not None)

        result = self.hue_put("/lights/{}/state".format(id), payload)
        parsed = json.loads(result)

        api_to_property_name_mapping = {
            'bri': 'brightness',
            'sat': 'saturation',
            'transitiontime': 'transition_time'
        }

        result = LightStateCommandResult()

        for call_result in parsed:
            if 'success' in call_result:
                url, state = call_result['success'].popitem()
                api_key = url[url.rfind('/') + 1:]
                propertyName = api_to_property_name_mapping.get(api_key, api_key)
                setattr(result, propertyName, state)

        return result


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


class Error(Exception):
    pass


class LightError(Error):
    def __init__(self, message):
        self.message = message


class Scan:
    def __init__(self, lastscan):
        self.lastscan = lastscan
        self.lights = []


class Light:
    def __init__(self, id, name=None):
        self.id = id
        self.name = name


class LightStateCommand:
    def __init__(self, on=None, brightness=None, hue=None, saturation=None, xy=None, color_temperature=None,
                 alert=None, effect=None, transition_time=None):
        vars(self).update(locals())


class LightStateCommandResult(LightStateCommand):
    pass


class LightState:
    def __init__(self, state=None, type=None, name=None, model_id=None, sw_version=None, point_symbol=None):
        vars(self).update(locals())


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
    def __init__(self, hue=None, on=None, effect=None, alert=None, brightness=None, saturation=None, ct=None, xy=None, reachable=None,
                 color_mode=None):
        vars(self).update(locals())


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
