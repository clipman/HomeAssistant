FROM python:3.7.3
ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh rs485.conf rs485.py /

# Install requirements for add-on
RUN python3 -m pip install pyserial
RUN python3 -m pip install paho-mqtt

WORKDIR /share
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
