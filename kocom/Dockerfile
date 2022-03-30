FROM python:3

ENV LANG C.UTF-8

RUN pip install --upgrade pip

RUN adduser -D myuser
USER myuser
WORKDIR /home/myuser

COPY --chown=myuser:myuser requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/user/.local/bin:${PATH}"

COPY --chown=myuser:myuser . .

#CMD ["python", "kocom.py", "runserver", "0.0.0.0:8000"]

# Install requirements for add-on
RUN apt-get update && apt-get -y install jq
RUN python3 -m pip install pyserial
RUN python3 -m pip install paho-mqtt

# Copy data for add-on
COPY run.sh kocom.conf kocom.py /

WORKDIR /share

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
