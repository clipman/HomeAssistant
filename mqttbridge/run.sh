#!/bin/sh

SHARE_DIR=/share

if [ ! -f $SHARE_DIR/mqttbridge.cfg ]; then
	mv /mqttbridge.cfg $SHARE_DIR
fi

echo "[Info] MQTT <-> TCP Bridge Server"

cd $SHARE_DIR
python3 /mqttbridge.py
