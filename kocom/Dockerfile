#ARG BUILD_FROM="alpine:latest"
ARG BUILD_FROM
FROM $BUILD_FROM
#FROM python:3

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh kocom.conf kocom.py /

# Install requirements for add-on
RUN apk add --no-cache jq npm make gcc g++ python3 linux-headers udev && \
    npm init -f && \
    npm install mqtt && \
    npm install serialport --build-from-source=serialport 

#RUN apt-get update && apt-get -y install jq
#RUN python3 -m pip install pyserial
#RUN python3 -m pip install paho-mqtt

WORKDIR /share
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
