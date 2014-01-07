import unittest
import time
import logging

from logging import Formatter

from HuetonApi.LightsApi import LightsApi
from HuetonApi.ConfigurationApi import ConfigurationApi


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        configuration_api = ConfigurationApi('huetonuser', 'http://192.168.2.196/api/')
        configuration_api.create_user('api', 'huetonuser')

        self.configuration_api = configuration_api
        self.light_api = LightsApi('huetonuser', 'http://192.168.2.196/api/')

        logger = logging.getLogger('hueton')
        logger.handlers = []  # clear handlers
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)

        self.logger = logger

    def test_scenario_diagnostics(self):
        lights = self.light_api.get_all_lights()
        [self.logger.debug(repr(light)) for light in lights]

    def test_configuration(self):
        self.logger.debug(self.configuration_api.get_configuration())

    def test_scenario_turn_lights_on_and_off(self):
        lights = self.light_api.get_all_lights()

        for _ in range(3):
            self.logger.debug("Turn lights off")
            [self.light_api.hue_turn_lamp_off(light.id) for light in lights]
            time.sleep(1)

            self.logger.debug("Turn lights on")
            [self.light_api.hue_turn_lamp_on(light.id) for light in lights]
            time.sleep(1)

    def test_colorize_light(self):
        lights = self.light_api.get_all_lights()

        for light in lights:
            print("light " + str(light.name))
            self.light_api.set_color(light.id, 255, 0, 0)
            time.sleep(1)
            self.light_api.set_color(light.id, 0, 255, 0)
            time.sleep(1)
            self.light_api.set_color(light.id, 0, 0, 255)
            time.sleep(1)



