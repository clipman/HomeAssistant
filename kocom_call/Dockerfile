FROM python:3
ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh kocom_call.conf kocom_call.py /

# Install requirements for add-on
RUN python3 -m pip install pyserial; exit 0
RUN python3 -m pip install paho-mqtt; exit 0

WORKDIR /share
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
