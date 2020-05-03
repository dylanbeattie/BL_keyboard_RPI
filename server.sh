#!/bin/bash
# remove the desktop pairing (we'll eventually fix this...)
# bluetoothctl remove `bluetoothctl devices | sed -e "s/Device \(..:..:..:..:..:..\).*/\1/g"`
sudo killall -9 bluetoothd
#Stop the background process
sudo /etc/init.d/bluetooth stop
# Turn on Bluetooth
sudo hciconfig hcio up
# Update  mac address
# ./updateMac.sh
#Update Name
# ./updateName.sh
sudo /usr/sbin/bluetoothd --nodetach --debug -p time &
sudo python server/btk_server.py


