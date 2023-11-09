#!/bin/sh

SHARE_DIR=/share

if [ ! -f $SHARE_DIR/edgebridge.cfg ]; then
	mv /edgebridge.cfg $SHARE_DIR
fi

echo "[Info] Bridge Server for SmartThings Edge drivers"

cd $SHARE_DIR
python3 /edgebridge.py
