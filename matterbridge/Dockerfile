ARG BUILD_FROM=ghcr.io/hassio-addons/base-nodejs:0.2.3
FROM $BUILD_FROM

ARG MATTERBRIDGE_HOME_ASSISTANT_VERSION

# webinterface
EXPOSE 8283
# Matter
EXPOSE 5540

RUN mkdir /app
WORKDIR /app

RUN \
    ln -s /config /root/.matterbridge && \
    npm install -g matterbridge@1.5.2 matterbridge-home-assistant@1.9.0 matterbridge-zigbee2mqtt@2.1.14

COPY run.sh run.sh
RUN chmod a+x run.sh

CMD [ "/app/run.sh" ]
