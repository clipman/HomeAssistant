#!/bin/sh

SHARE_DIR=/share/kocom

if [ ! -f $SHARE_DIR/kocom_call.conf ]; then
	mkdir $SHARE_DIR
	mv /kocom_call.conf $SHARE_DIR
fi

echo "[Info] Run Kocom Call with RS485..."

python3 /kocom_call.py

# for dev
while true; do echo "still live"; sleep 100; done
