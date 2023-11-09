FROM python:3.6
COPY run.sh edgebridge.cfg edgebridge.py /
RUN pip install requests==2.26.0
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
