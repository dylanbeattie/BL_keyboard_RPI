#! /bin/bash
a="\"`cat /proc/cpuinfo | grep -P "Model\t+:" | sed -e "s/^Model\t*: //g"`\""
sed -i -e "s/\(MY_DEV_NAME=\).*/\1$a/" server/btk_server.py



