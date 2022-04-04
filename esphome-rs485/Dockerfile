ARG BUILD_FROM=esphome/esphome-hassio-base-amd64:2.5.0
FROM ${BUILD_FROM}

# Copy root filesystem
COPY rootfs /

RUN pip3 install --no-cache-dir https://github.com/reflican/esphome/archive/master.zip

# Labels
LABEL \
    io.hass.type="addon" \
    io.hass.version=rs485
