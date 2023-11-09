FROM python:3
RUN pip install requests==2.26.0
COPY edgebridge.py edgebridge.cfg /share/
WORKDIR /share
CMD [ "python", "edgebridge.py" ]
