FROM python:3
COPY run.sh edgebridge.cfg edgebridge.py /
RUN python3 -m pip install requests
WORKDIR /share
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
