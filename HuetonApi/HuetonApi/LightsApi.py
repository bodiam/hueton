from HuetonApi.HueApi import HueApi
import json


class LightsApi(HueApi):
    def init(self, developer_name):
        print("Hello %s" % developer_name)
        self.base_location = "http://192.168.2.196/api/"
        self.location = self.base_location + developer_name
        self.developer_name = developer_name

    def get_all_lights(self):
        result = self.hue_get("/lights")
        parsed = json.loads(result)

        return [Light(id, parsed[id]["name"]) for id in parsed]


class Light:
    def __init__(self, id, name):
        self.id = id
        self.name = name


