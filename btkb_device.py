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

from btkb_bluezprofile import BTKbBluezProfile

class BTKbDevice():
	#change these constants
	MY_ADDRESS="B8:27:EB:CB:A7:0B"
	MY_DEV_NAME="dylan-pi-zero"

	#define some constants
	P_CTRL =17  #Service port - must match port configured in SDP record
	P_INTR =19  #Service port - must match port configured in SDP record#Interrrupt port
	PROFILE_DBUS_PATH="/bluez/yaptb/btkb_profile" #dbus path of  the bluez profile we will create
	SDP_RECORD_PATH = sys.path[0] + "/sdp_record.xml" #file path of the sdp record to laod
	UUID="00001124-0000-1000-8000-00805f9b34fb"

	def __init__(self):
		print("Setting up BT device")
		self.init_bluez_profile()

	#set up a bluez profile to advertise device capabilities from a loaded service record
	def init_bluez_profile(self):
		print("Configuring Bluez Profile")

		#setup profile options
		service_record=self.read_sdp_service_record()
		opts = {
			"ServiceRecord":service_record,
			"Role":"server",
			"RequireAuthentication":False,
			"RequireAuthorization":False
		}

		#retrieve a proxy for the bluez profile interface
		bus = dbus.SystemBus()
		manager = dbus.Interface(bus.get_object("org.bluez","/org/bluez"), "org.bluez.ProfileManager1")
		profile = BTKbBluezProfile(bus, BTKbDevice.PROFILE_DBUS_PATH)
		manager.RegisterProfile(BTKbDevice.PROFILE_DBUS_PATH, BTKbDevice.UUID,opts)
		print("Profile registered ")

	#read and return an sdp record from a file
	def read_sdp_service_record(self):
		print("Reading service record")
		try:
			fh = open(BTKbDevice.SDP_RECORD_PATH, "r")
		except:
			sys.exit("Could not open the sdp record. Exiting...")
		return fh.read()

	#listen for incoming client connections
	#ideally this would be handled by the Bluez 5 profile
	#but that didn't seem to work
	def listen(self):
		print("Waiting for connections")
		self.scontrol=BluetoothSocket(L2CAP)
		self.sinterrupt=BluetoothSocket(L2CAP)

		#bind these sockets to a port - port zero to select next available
		self.scontrol.bind((self.MY_ADDRESS,self.P_CTRL))
		self.sinterrupt.bind((self.MY_ADDRESS,self.P_INTR ))

		#Start listening on the server sockets
		self.scontrol.listen(1) # Limit of 1 connection
		self.sinterrupt.listen(1)

		self.ccontrol,cinfo = self.scontrol.accept()
		print ("Got a connection on the control channel from " + cinfo[0])

		self.cinterrupt, cinfo = self.sinterrupt.accept()
		print ("Got a connection on the interrupt channel from " + cinfo[0])


	#send a string to the bluetooth host machine
	def send_string(self,message):

	 #    print("Sending "+message)
		 self.cinterrupt.send(message)


