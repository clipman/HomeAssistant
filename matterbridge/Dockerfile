ARG BUILD_FROM=ghcr.io/hassio-addons/base-nodejs:d6f5a5a
FROM $BUILD_FROM

EXPOSE 8283
EXPOSE 5540

RUN mkdir /app
WORKDIR /app

RUN \
    ln -s /config /root/.matterbridge \
    && npm install -g matterbridge --omit=dev \
    && npm install -g matterbridge-home-assistant --omit=dev \
    && npm install -g matterbridge-zigbee2mqtt --omit=dev

COPY run.sh run.sh
RUN chmod a+x run.sh

CMD [ "/app/run.sh" ]
