import requests
import json

from HuetonApi.HueApi import HueApi

class HuetonApi(HueApi):
    def init(self, developer_name):
        print("Hello %s" % developer_name)
        self.registered = False
        self.base_location = "http://192.168.2.196/api/"
        self.location = self.base_location + developer_name
        self.developer_name = developer_name

    def connect(self):

        result = self.hue_get("")
        parsed = json.loads(result)
        return 'success' in parsed[0]

    def register(self):
        print("Please press the button on the hub.")

        payload = json.dumps({"devicetype": "test user", "username": self.developer_name})
        response = requests.post(self.base_location, data=payload)

        print(response)

        self.registered = True

