ARG BUILD_FROM=esphome/esphome-hassio-base-amd64:3.0.0
FROM ${BUILD_FROM}

# Copy root filesystem
COPY rootfs /

RUN pip3 install --no-cache-dir https://github.com/esphome/home-assistant-addon/archive/refs/tags/v1.18.0.zip

# Labels
LABEL \
    io.hass.type="addon" \
    io.hass.version=rs485
