#!/bin/sh

SHARE_DIR=/share
if [ ! -f $SHARE_DIR/kocom.cfg ]; then
	mv /kocom.cfg $SHARE_DIR
fi

echo "[Info] Run Kocom Wallpad with RS485..."

cd $SHARE_DIR
python3 /kocom.py
