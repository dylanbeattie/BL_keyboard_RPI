#!/usr/bin/python

from __future__ import absolute_import, print_function

from optparse import OptionParser, make_option
import os
import sys
import uuid
import dbus
import dbus.service
import dbus.mainloop.glib
import time
import bluetooth
from bluetooth import *

from dbus.mainloop.glib import DBusGMainLoop
from btkb_service import BTKbService

def initialize_bluetooth():
	DEVICE_NAME = "dylan-pi-zero-w"

	# Turn it off...
	os.system("/etc/init.d/bluetooth stop")
	# ...and on again.
	# os.system("/etc/init.d/bluetooth start")

	# os.system("hciconfig hcio up")
	# start the bluetooth daemon. I don't know why this is required. (yet)
	os.system("/usr/sbin/bluetoothd --nodetach --debug -p time &")
	print("Waiting 5 seconds because bad things happen if we don't...")
	time.sleep(5)
	# set the device class to a keybord and set the name
	os.system("hciconfig hci0 up")
	os.system("hciconfig hcio class 0x002540")
	os.system("hciconfig hcio name " + DEVICE_NAME)
	# make the device discoverable
	os.system("hciconfig hcio piscan")


#main routine
if __name__ == "__main__":
	# we an only run as root
	if not os.geteuid() == 0:
	   sys.exit("Only root can run this script")

	initialize_bluetooth()

	DBusGMainLoop(set_as_default=True)
	myservice = BTKbService()
	gtk.main()
