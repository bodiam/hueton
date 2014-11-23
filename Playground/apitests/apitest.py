import requests
import json
import sys
import ConfigParser

from collections import defaultdict

config = ConfigParser.RawConfigParser()
config.read('ConfigFile.properties')

bridge = config.get('HuetonApi', 'bridge.ip');

location = "http://"+ bridge +"/api/newdeveloper"

#
# Hue API
#
def hue_get_lamp_state(lamp_number):
    result = hue_get("/lights/" + lamp_number)
    parsed = json.loads(result)
    state = parsed['state']['on']

    return state


def hue_set_lamp_color(lamp_number, saturation, brightness, hue):
    # {"on":true, "sat":255, "bri":255,"hue":10000}
    payload = json.dumps({"on": True, "sat": int(saturation), "bri": int(brightness), "hue": int(hue)})
    hue_set_lamp_state(lamp_number, payload)


def hue_turn_lamp_on(lamp_number):
    payload = json.dumps({"on": True})
    hue_set_lamp_state(lamp_number, payload)


def hue_turn_lamp_off(lamp_number):
    payload = json.dumps({"on": False})
    hue_set_lamp_state(lamp_number, payload)


def hue_set_lamp_state(lamp_number, payload):
    hue_put("/lights/" + lamp_number + "/state", payload)


def hue_get(function):
    return requests.get(location + function).text


def hue_put(function, payload):
    return requests.put(location + function, data=payload)

#
# Main programs
#
def clear_screen():
    print

#print chr(27) + "[2J"

def show_menu():
    menu = defaultdict(list, {
    '1': [register_new_user, 'Register new user'],
    '2': [show_all_lamps, 'Show all lamps'],
    '3': [show_turn_lamps_on_off, 'Turn lamps on/off'],
    '4': [show_colorize_lamps, 'Colorize lamps'],
    '5': [use_leapmotion, 'Use leapmotion'],
    '6': [show_bridge, 'Show bridge'],
    'E': [sys.exit, 'Exit']
    })

    print("")
    for key in sorted(menu.keys()):
        print("%s : %s" % (key, menu[key][1]))

    choice = input("Please choose a number: ")

    if not menu[choice]:
        print("Invalid input: %s" % choice)
        show_menu()

    clear_screen()

    func = menu[choice][0]
    func()


def register_new_user():
    print("register new user")
    show_menu()


def show_all_lamps():
    print_lamps()

    show_menu()


def print_lamps():
    title("Show all lamps")

    # {"1":{"name": "Hue Lamp 1"},"2":{"name": "Hue Lamp 2"},"3":{"name": "Hue Lamp 3"}}
    result = hue_get("/lights")
    parsed = json.loads(result)

    for key in sorted(parsed.keys()):
        state = hue_get_lamp_state(key)
        print("lamp:%s, name=%s, state=%s" % (key, parsed[key]['name'], state))


def title(text):
    print(text + ":\n")


def show_turn_lamps_on_off():
    title("Turn lamps [on/off]:")

    print_lamps()

    # Choose the lamp
    lamp_number = get_input_lamp_number()
    state = hue_get_lamp_state(lamp_number)

    # Choose the action
    input = input("Turn lamp %s [on] or [off]: " % lamp_number)

    if input == "on":
        hue_turn_lamp_on(lamp_number)
    else:
        hue_turn_lamp_off(lamp_number)

    show_turn_lamps_on_off()


def get_input_lamp_number():
    lamp_number = input("Please choose a lamp number (E=Exit menu): ")

    if not lamp_number:
        show_turn_lamps_on_off()

    if lamp_number == "E":
        show_all_lamps()

    return lamp_number


def show_colorize_lamps():
    title("Colorize lamps")

    print_lamps()

    # Choose the lamp
    lamp_number = get_input_lamp_number()

    # TODO: read current lamp settings

    # Choose the action
    saturation = read_input("Saturation (intesity) [0-255] :") or '255'
    brightness = read_input("Brightness [0-255] :") or '255'
    hue = read_input("Hue [0-65535] :") or '10000'

    hue_set_lamp_color(lamp_number, saturation, brightness, hue)

    show_menu()


def use_leapmotion():
    print("Use leapmotion")
    show_menu()

def show_bridge():
    print("bridge :"+ bridge)
    show_menu()

def read_input(text):
    return input(text)


show_menu()



