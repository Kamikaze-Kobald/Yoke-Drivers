#!/usr/bin/python
import struct
import time
import sys
from evdev import UInput, ecodes as e
import os

infile_path = '/dev/input/by-id/usb-Logitech_Logitech_Extreme_3D-event-joystick'


FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

#open file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)

types = ['SEPARATOR', 'KEY', 'RELATIVE AXIS', 'ABSOLUTE AXIS', 'OTHER']
buttons = {
	0: 'steer wheel',
	1: 'piston',
	2: 'throttle 1',
	3: 'throttle 3',
	4: 'throttle 2',
	16: 'dpad hori',
	17: 'dpad vert',
	288: 'left trigger',
	289: 'right trigger',
	290: 'hori pad left',
	291: 'hori pad right',
	292: 'left switch up',
	293: 'left switch down',
	294: 'right switch up',
	295: 'right switch down',
	296: 'top red',
	297: 'bottom red',
	298: 'vert pad up',
	299: 'vert pad down',
}

capabilities = {
	e.EV_KEY: [
		e.KEY_W,
		e.KEY_S,
		e.KEY_D,
		e.KEY_A,
	]
}

keymap = {
	298: e.KEY_W,
	299: e.KEY_S,
	290: e.KEY_A,
	291: 32
}

ui = UInput(capabilities, name='yoke-driver')

keylist = {}

while event:
	(tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
	if code in buttons.keys() and code > 1 and type != 4:
		keylist[buttons[code]] = value

	elif type != 0 and code > 1 and type != 4:
		keylist[code] = value
	if code in keymap.keys():
		ui.write(e.EV_KEY, keymap[code], value)
		ui.write(0, 0, 0)
		keylist[keymap[code]] = value
	event = in_file.read(EVENT_SIZE)
	os.system('clear')
	for i in keymap.keys():
		print(i, keymap[i])

in_file.close()

