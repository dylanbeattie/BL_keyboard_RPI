# Requirements (covers multiple versions of Python):
# apt-get install python-requests python3-requests

import RPi.GPIO as GPIO
import time
import requests
from time import sleep
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Raspberry GPIO Configuration
gpiopin = 21

GPIO.setmode(GPIO.BCM)
for pin in range(1,21):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prev_states = [False] * 27
while True:
    for pin in range(1,21):
        state = GPIO.input(pin)
        prev_state = prev_states[pin]
        if (state != prev_state):
            print("Pin", pin, "now", state)
            prev_states[pin] = state
    # if state == False and previous == "open" or state == False and previous == "null":
    #     print('Circuit Closed.')
    #     previous = "closed"
    # if state != False and previous == "closed" or state != False and previous == "null":
    #     print('Circuit Open.')
    #     previous = "open"
    
for pin in range(1,21):
    GPIO.cleanup(pin)