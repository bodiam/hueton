import json
from HuetonApi.HueApi import HueApi
import time


class ConfigurationApi(HueApi):
    LINK_BUTTON_NOT_PRESSED_ERROR = 101

    def create_user(self, device_type, username=None):

        configuration = self.get_configuration()
        if configuration.gateway is not None:
            return

        payload = json.dumps({"devicetype": device_type, "username": username})

        max_attempts = 5
        for attempt in range(max_attempts):
            print("Please press the link button on the bridge ({}/{})".format(attempt + 1, max_attempts))
            result = self.raw_post(payload)
            parsed = json.loads(result)

            if "success" in parsed[0]:
                break
            elif parsed[0]['error']['type'] == ConfigurationApi.LINK_BUTTON_NOT_PRESSED_ERROR:
                time.sleep(5)
            else:
                message = "Error {}".format(parsed[0]['error']['type'])
                raise Exception(message)

        raise Exception("No button was pressed")

    def get_configuration(self):

        parsed = self.hue_get("/config")
        return Configuration(**parsed)

    def modify_configuration(self, configuration):
        # payload = json.dumps(configuration, default=lambda c: c.__dict__)
        payload = json.dumps(configuration.__dict__)
        parsed = self.hue_put("/config", payload)
        return Configuration(**parsed)

    def delete_user_from_whitelist(self):
        pass

    def get_full_state(self):
        pass


class Configuration:
    def __init__(self, proxyport=None, UTC=None, name=None, swupdate=None, whitelist=None, swversion=None, proxyaddress=None,
                 mac=None, linkbutton=None, ipaddress=None, netmask=None, gateway=None, dhcp=None, portalservices=None):
        vars(self).update(dict([entry for entry in locals().items() if entry[0] is not 'self']))



