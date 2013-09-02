import requests
import json

class HueApi:
    def hue_get_lamp_state(self, lamp_number):
        result = self.hue_get("/lights/" + lamp_number)
        parsed = json.loads(result)
        state = parsed['state']['on']

        return state

    def hue_set_lamp_color(self, lamp_number, saturation, brightness, hue):
        # {"on":true, "sat":255, "bri":255,"hue":10000}
        payload = json.dumps({"on": True, "sat": int(saturation), "bri": int(brightness), "hue": int(hue)})
        self.hue_set_lamp_state(lamp_number, payload)

    def hue_turn_lamp_on(self, lamp_number):
        payload = json.dumps({"on": True})
        self.hue_set_lamp_state(lamp_number, payload)

    def hue_turn_lamp_off(self, lamp_number):
        payload = json.dumps({"on": False})
        self.hue_set_lamp_state(lamp_number, payload)

    def hue_set_lamp_state(self, lamp_number, payload):
        self.hue_put("/lights/" + lamp_number + "/state", payload)

    def hue_get(self, function):
        return requests.get(self.location + function).text

    def hue_put(self, function, payload):
        return requests.put(self.location + function, data=payload)

    def hue_post(self, function, payload):
        return requests.post(self.location + function, data=payload)
