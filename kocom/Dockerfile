FROM python:3

ENV LANG C.UTF-8

RUN pip install --upgrade pip

# Install requirements for add-on
RUN apt-get update && apt-get -y install jq
RUN python3 -m pip install pyserial
RUN python3 -m pip install paho-mqtt

# Copy data for add-on
COPY run.sh kocom.conf kocom.py /

WORKDIR /share

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
