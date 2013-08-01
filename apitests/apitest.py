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
	        '3':[show_turn_lamps_on_off,'Turn lamps on/off'],
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



def register_new_user():

	print "register new user"
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
                print "lamp:%s, name=%s, state=%s" % (key, parsed[key]['name'], state)

def title(text): 
	print text + ":\n"


def hue_get_lamp_state(lamp_number):

	result = hue_get("/lights/" + lamp_number)
	parsed = json.loads(result)
	state = parsed['state']['on']

	return state	

def hue_turn_lamp_on(lamp_number):
	payload = json.dumps({"on":True})
	hue_set_lamp_state(lamp_number, payload)

def hue_turn_lamp_off(lamp_number):
	payload = json.dumps({"on":False})
	hue_set_lamp_state(lamp_number, payload)

def hue_set_lamp_state(lamp_number, payload):
	hue_put("/lights/"+ lamp_number + "/state", payload)

def hue_get(function):
	return requests.get(location + function).content

def hue_put(function, payload):
	return requests.put(location + function, data=payload)


def show_turn_lamps_on_off():

	title("Turn lamps [on/off]:")

	print_lamps()
		
	# Choose the lamp
	lamp_number = get_input_lamp_number()
	state = hue_get_lamp_state(lamp_number)

	# Choose the action
	input = raw_input("Turn lamp %s [on] or [off]: " % lamp_number)

	if input == "on":
		hue_turn_lamp_on(lamp_number)
	else:
		hue_turn_lamp_off(lamp_number)

	show_turn_lamps_on_off()

def get_input_lamp_number():
	lamp_number = raw_input("Please choose a lamp number (E=Exit menu): ")

	if not lamp_number:
		turn_lamps_on_off()

	if lamp_number == "E":
		show_all_lamps()

	return lamp_number


def colorize_lamps():

	print "Colorize lamps"
	show_menu()

def use_leapmotion():
	print "Use leapmotion"
	show_menu()

show_menu()


