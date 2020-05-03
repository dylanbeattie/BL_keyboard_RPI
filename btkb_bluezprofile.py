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

#
#define a bluez 5 profile object for our keyboard
#
class BTKbBluezProfile(dbus.service.Object):
	fd = -1

	@dbus.service.method("org.bluez.Profile1", in_signature="", out_signature="")
	def Release(self):
		print("Release")
		mainloop.quit()

	@dbus.service.method("org.bluez.Profile1", in_signature="", out_signature="")
	def Cancel(self):
		print("Cancel")

	@dbus.service.method("org.bluez.Profile1", in_signature="oha{sv}", out_signature="")
	def NewConnection(self, path, fd, properties):
		self.fd = fd.take()
		print("NewConnection(%s, %d)" % (path, self.fd))
		for key in properties.keys():
			if key == "Version" or key == "Features":
				print("  %s = 0x%04x" % (key, properties[key]))
			else:
				print("  %s = %s" % (key, properties[key]))

	@dbus.service.method("org.bluez.Profile1", in_signature="o", out_signature="")
	def RequestDisconnection(self, path):
		print("RequestDisconnection(%s)" % (path))

		if (self.fd > 0):
			os.close(self.fd)
			self.fd = -1

	def __init__(self, bus, path):
		dbus.service.Object.__init__(self, bus, path)