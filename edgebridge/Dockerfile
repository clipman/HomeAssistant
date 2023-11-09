FROM python:3
COPY run.sh edgebridge.cfg edgebridge.py /
RUN pip install --no-cache-dir -r requests==2.26.0
WORKDIR /share
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
