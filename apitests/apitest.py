import requests
import json
import sys

from collections import defaultdict

location = "http://192.168.2.196/api/newdeveloper"

def clear_screen():
	print chr(27) + "[2J"

def show_menu():

	menu = defaultdict(list, { 
		'1':[register_new_user,'Register new user'],
		'2':[show_all_lamps,'Show all lamps'],
	        '3':[turn_lamps_on_off,'Turn lamps on/off'],
	        '4':[colorize_lamps,'Colorize lamps'],
	        '5':[use_leapmotion,'Use leapmotion'],
	        'E':[sys.exit, 'Exit']
	})

	print ""
	for key in sorted(menu.keys()):
		print "%s : %s" % (key, menu[key][1])

	choice = raw_input("Please choose a number: ")

	if not menu[choice]:
		print "Invalid input: %s" % choice
		show_menu()

	clear_screen()

	func = menu[choice][0]
	func()


def get(function):
	return requests.get(location + function).content

def register_new_user():

	print "register new user"
	show_menu()

def show_all_lamps():

	_print_lamps()

	show_menu()

def _print_lamps():

        # {"1":{"name": "Hue Lamp 1"},"2":{"name": "Hue Lamp 2"},"3":{"name": "Hue Lamp 3"}}
        result = get("/lights")

        parsed = json.loads(result)

        print "Show all lamps:\n"

        for key in sorted(parsed.keys()):
                print "%s = %s" % (key, parsed[key]['name'])

def turn_lamps_on_off():

	print "Turn lamps on / off:"

	_print_lamps()

	lamp_number = raw_input("Please choose a lamp number (E=Exit menu): ")

	if not lamp_number:
		turn_lamps_on_off()

	if lamp_number == "E":
		show_all_lamps()

	result = get("/lights/" + lamp_number)

	parsed = json.loads(result)
	state = parsed['state']['on']

	if state:
		message = "Lamp is on. [on/off]"
	else:
		message = "Lamp is off. [on/off]"

	input = raw_input(message)

	if input == "on":
		payload = json.dumps({"on": True})
	else:
		payload = json.dumps({"on": False})

	r = requests.put("http://192.168.2.196/api/newdeveloper/lights/" + lamp_number + "/state", data = payload)

	turn_lamps_on_off()

def colorize_lamps():

	print "Colorize lamps"
	show_menu()

def use_leapmotion():
	print "Use leapmotion"
	show_menu()

show_menu()


