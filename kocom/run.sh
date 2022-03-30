#!/bin/sh

python3 -m pip install pyserial
python3 -m pip install paho-mqtt

#SHARE_DIR=/share/kocom
SHARE_DIR=/config/custom_components/kocom

if [ ! -f $SHARE_DIR/kocom.py ]; then
	mkdir $SHARE_DIR
	mv /kocom.py $SHARE_DIR
	mv /kocom.conf $SHARE_DIR
fi

echo "[Info] Run Kocom Wallpad with RS485!"
cd $SHARE_DIR
python3 $SHARE_DIR/kocom.py

# for dev
while true; do echo "still live"; sleep 100; done
