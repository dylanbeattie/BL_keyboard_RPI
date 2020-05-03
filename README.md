# Dylan's Hardware Pi Hack Footpedal Keyboard Bluetooth Experiment

This is so work-in-progress it's a miracle it runs at all... but it works.

1. Run sudo ./server.sh on the Pi Zero
2. Open Bluetooth on your host PC/Mac, delete ANY PREVIOUS INSTANCES of the Pi, then add new device
3. Once it's paired, connected and ready to go, run ./client.sh

To send the keystroke 'a', connect GPIO pin 2 to ground.
To send the keystroke 'b', connect GPIO pin 3 to ground.
To send the keystroke 'c', connect GPIO pin 4 to ground.

That's... all for now. More coming soon.