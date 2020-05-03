
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

from btkb_device import BTKbDevice

#define a dbus service that emulates a bluetooth keyboard
#this will enable different clients to connect to and use
#the service
class BTKbService(dbus.service.Object):

	def __init__(self):

		print("Setting up service")

		#set up as a dbus service
		bus_name=dbus.service.BusName("org.yaptb.btkbservice",bus=dbus.SystemBus())
		dbus.service.Object.__init__(self,bus_name,"/org/yaptb/btkbservice")

		#create and setup our device
		self.device= BTKbDevice()

		#start listening for connections
		self.device.listen()

	@dbus.service.method('org.yaptb.btkbservice', in_signature='yay')
	def send_keys(self,modifier_byte,keys):

		cmd_str=""
		cmd_str+=chr(0xA1)
		cmd_str+=chr(0x01)
		cmd_str+=chr(modifier_byte)
		cmd_str+=chr(0x00)

		count=0
		for key_code in keys:
			if(count<6):
				cmd_str+=chr(key_code)
			count+=1
		
		print ("self.device.send_string(" + cmd_str + ")")

		self.device.send_string(cmd_str)

