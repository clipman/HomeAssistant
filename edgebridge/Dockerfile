FROM python:3
RUN pip install requests==2.26.0
COPY edgebridge.py /
COPY edgebridge.cfg /
RUN mkdir /share
RUN mkdir /share/edgebridge
RUN mv /edgebridge.py /share/edgebridge/
RUN mv /edgebridge.cfg /share/edgebridge/
WORKDIR /share/edgebridge
CMD [ "python", "edgebridge.py" ]
