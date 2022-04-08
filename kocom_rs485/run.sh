#!/bin/sh

SHARE_DIR=/share/kocom

if [ ! -f $SHARE_DIR ]; then
	mkdir $SHARE_DIR
	mv /rs485.conf $SHARE_DIR
fi

echo "[Info] Run Kocom Wallpad with RS485..."

cd $SHARE_DIR
python3 /rs485.py

# for dev
while true; do echo "still live"; sleep 100; done
