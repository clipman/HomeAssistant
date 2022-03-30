#ARG BUILD_FROM=multiarch/debian-debootstrap:amd64-stretch
ARG BUILD_FROM
FROM $BUILD_FROM
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -y install jq
RUN pip3 install --upgrade pip
COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade six

# Install requirements for add-on
RUN python3 -m pip install pyserial
RUN python3 -m pip install paho-mqtt

RUN apt-get clean -y
RUN rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND newt
ENV PYTHONIOENCODING utf-8

# Copy data for add-on
COPY run.sh kocom.conf kocom.py /

RUN chmod a+x /run.sh

WORKDIR /share

ENTRYPOINT [ "/run.sh" ]
