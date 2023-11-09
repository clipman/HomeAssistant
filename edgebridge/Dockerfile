FROM python:3
WORKDIR /share
RUN pip install requests==2.26.0
COPY edgebridge.py edgebridge.cfg .
CMD [ "python", "edgebridge.py" ]
