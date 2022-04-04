ARG BUILD_FROM=esphome/esphome-hassio-amd64:dev
FROM ${BUILD_FROM}

# Copy root filesystem
COPY rootfs /

RUN pip3 install --no-cache-dir https://github.com/esphome/esphome/archive/refs/tags/2022.1.4.zip

# Labels
LABEL \
    io.hass.type="addon" \
    io.hass.version=dev
