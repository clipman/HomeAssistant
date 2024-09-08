# ARG BUILD_FROM=ghcr.io/hassio-addons/base-nodejs:0.2.3
# FROM $BUILD_FROM
FROM node:18

EXPOSE 8283
EXPOSE 5540

#RUN mkdir /app
WORKDIR /app

RUN \
    ln -s /config /root/.matterbridge \
    && npm install -g matterbridge@1.5.2 \
    && npm install -g matterbridge-home-assistant@2.9.0 \
    && npm install -g matterbridge-zigbee2mqtt@2.1.14 \
    && matterbridge -add matterbridge-home-assistant \
    && matterbridge -add matterbridge-zigbee2mqtt

COPY run.sh run.sh
RUN chmod a+x run.sh

CMD [ "/app/run.sh" ]
