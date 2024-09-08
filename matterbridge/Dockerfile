ARG BUILD_FROM=ghcr.io/hassio-addons/base-nodejs:d6f5a5a
FROM $BUILD_FROM

# webinterface
EXPOSE 8283
# Matter
EXPOSE 5540

RUN mkdir /app
WORKDIR /app

RUN \
    ln -s /config /root/.matterbridge && \
    npm install -g matterbridge@1.5.4 matterbridge-home-assistant matterbridge-zigbee2mqtt@2.1.14

COPY run.sh run.sh
RUN chmod a+x run.sh

CMD [ "/app/run.sh" ]
