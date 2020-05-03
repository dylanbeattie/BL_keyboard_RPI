#Stop the background process
sudo /etc/init.d/bluetooth stop
# disable bluetooth PIN code
sudo hciconfig noauth
# Turn on Bluetooth
sudo hciconfig hcio up
sudo python server/btk_server.py &
bluetoothctl agent on
bluetoothctl default-agent
bluetoothctl discoverable on
sudo python keyboard/kb_client.py
