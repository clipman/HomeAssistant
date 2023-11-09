#!/bin/sh

SHARE_DIR=/share/edgebridge

if [ ! -f $SHARE_DIR/edgebridge.cfg ]; then
	mkdir $SHARE_DIR
	mv /edgebridge.cfg $SHARE_DIR
fi

echo "[Info] Bridge Server for SmartThings Edge drivers"

cd $SHARE_DIR
python3 /edgebridge.py

# for dev
while true; do echo "Running..."; sleep 100; done
