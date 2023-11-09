FROM python:3
RUN pip install requests==2.26.0
RUN mkdir /share/edgebridge
COPY edgebridge.py edgebridge.cfg /share/edgebridge/
WORKDIR /share/edgebridge
CMD [ "python", "edgebridge.py" ]
