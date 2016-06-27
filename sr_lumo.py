
import speech_recognition as sr
from pyaudio import *
from functools import partial
import os, time

R = sr.Recognizer()
mic = sr.Microphone()

#- gen config object -
class obj:
	def __init__(self):
		pass

def genConfig():
	global config
	config = obj()
	config.quit = False
	config.asleep = False
	config.keys = ["Lux", "lux", "lucks", "locks", "Luxor"]
	config.keyed = False
	config.complete = True

	#- prep gpio pins -
	os.system("gpio -g mode 17 out")
	os.system("gpio -g mode 18 out")
	os.system("gpio -g mode 21 out")
	config.color_pin = {"green":"17", "red":"18", "blue":"21"}
	config.led_state = {"green":0, "red":0, "blue":0}

	config.command_resp = {
		"on red LED" : partial(switchLED,'red',1),
		"off red LED" : partial(switchLED,"red",0),
		"toggle red LED" : partial(switchLED,"red"),
		"on blue LED" : partial(switchLED,"blue",1),
		"off blue LED" : partial(switchLED,"blue",0),
		"toggle blue LED" : partial(switchLED,"blue"),
		"nevermind" : nevermind,
		"quit listening" : quitListening
		}

def keyCommand(command):
	global config
	c = command.split(' ')
	config.keyed = c[0] in config.keys
	if config.keyed:
		config.complete = False
		switchLED("green",1)

def parseCommand(command):
	global config
	for c in config.command_resp:
		if c in command:
			config.command_resp[c]()
			config.complete = True

	if config.complete == True:
		nevermind()

def switchLED(color,toggle=2):
	global config
	if toggle in [0,1]:
		if config.led_state == toggle:
			return #kill
		os.system("gpio -g write "+config.color_pin[color]+" "+str(toggle))
		config.led_state[color] = toggle
	else:
		os.system("gpio -g write "+config.color_pin[color]+" "+str(1-config.led_state[color]))
		config.led_state[color] = 1-config.led_state[color]

def nevermind():
	global config
	config.keyed = False
	config.complete = True
	switchLED("green",0)

def quitListening():
	global config
	nevermind()
	switchLED("red",0)
	switchLED("blue",0)
	config.quit = True

#---LOOP---
def execute():
	global config
	genConfig()
	config.quit = False
	while not config.quit:
		raw = listening()
		command = translate(raw)
		keyCommand(command)
		parseCommand(command)

def listening():
	global config
	print config.keyed
	with mic as source:
		print ""
		print "-- Listening... --"
		raw = R.listen(source)
		return raw

def translate(raw):
	try:
		command = R.recognize_google(raw)
		print "heard:", command
	except sr.UnknownValueError:
		command = "value_error"
		print "value_error"
	except sr.RequestError:
		command = "request_error"
		print "request_error"
	return command

def squawk():
    global config
	while True:
		raw = listening()
		command = translate(raw)
		print command

#execute()
