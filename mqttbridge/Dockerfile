FROM python:3.7.3
COPY run.sh mqttbridge.cfg mqttbridge.py /
RUN pip install paho-mqtt==1.6.1
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
