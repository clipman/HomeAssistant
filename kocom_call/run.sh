#!/bin/sh

SHARE_DIR=/share

if [ ! -f $SHARE_DIR/kocom_call.cfg ]; then
	mv /kocom_call.cfg $SHARE_DIR
fi

echo "[Info] Run Kocom Call with RS485..."

cd $SHARE_DIR
python3 /kocom_call.py
