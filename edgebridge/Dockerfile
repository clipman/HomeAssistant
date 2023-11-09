FROM python:3.12.0
COPY run.sh edgebridge.cfg edgebridge.py /
RUN pip install requests
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
