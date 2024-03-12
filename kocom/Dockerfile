FROM python:3.7.3
ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh kocom.cfg kocom.py /

# Install requirements for add-on
RUN pip install pyserial
RUN pip install paho-mqtt
RUN pip install typing_extensions

WORKDIR /share
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
