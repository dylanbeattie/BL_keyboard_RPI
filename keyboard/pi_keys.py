#!/usr/bin/python
import os #used to all external commands
import sys # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import time
import evdev # used to get input from the keyboard
from evdev import *
import keymap # used to map evdev input to hid keodes
import RPi.GPIO as GPIO
from time import sleep

#Define a client to listen to local key events
class Keyboard():

    def __init__(self):
        #the structure for a bt keyboard input report (size is 10 bytes)

        self.state=[
            0xA1, #this is an input report
            0x01, #Usage report = Keyboard
            #Bit array for Modifier keys
            [0,    #Right GUI - Windows Key
             0,    #Right ALT
             0,    #Right Shift
             0,    #Right Control
             0,    #Left GUI
             0,    #Left ALT
             0,    #Left Shift
             0],   #Left Control
            0x00,  #Vendor reserved
            0x00,  #rest is space for 6 keys
            0x00,
            0x00,
            0x00,
            0x00,
            0x00]

        print "setting up DBus Client"

        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object('org.yaptb.btkbservice','/org/yaptb/btkbservice')
        self.iface = dbus.Interface(self.btkservice,'org.yaptb.btkbservice')


    #poll for keyboard events
    def event_loop(self):
        prev_states = [False] * 27
        while True:
            for pin in range(1,21):
                state = GPIO.input(pin)
                prev_state = prev_states[pin]
                if (state != prev_state):
                    prev_states[pin] = state
                    if (state == 0): # key DOWN
                        print("Sending keyDOWN for pin ", pin)
                        self.iface.send_keys(0, [pin+2,0,0,0,0,0])
                    if (state == 1):
                        print("Sending keyUp for pin ", pin)
                        self.iface.send_keys(0, [0,0,0,0,0,0])
                        
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    for pin in range(1,21):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    kb = Keyboard()
    print "starting event loop"
    kb.event_loop()

    for pin in range(1,21):
        GPIO.cleanup(pin)
