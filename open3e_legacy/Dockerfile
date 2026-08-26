ARG BUILD_FROM=ghcr.io/home-assistant/base-python:3.14-alpine3.23
FROM $BUILD_FROM


RUN apk update && apk add --no-cache bash git iproute2 nginx ttyd
RUN mkdir -p /data /run/nginx
WORKDIR /data

# Pinned upstream develop (2026-08): includes the O3ESwitch ZigBee room device
# codec (per-device-type decode) that fixes wrong ActualTemperature values.
RUN pip install "open3e @ git+https://github.com/open3e/open3e.git@2375e95e3f274d6c828d05d13e5227964c1e5f2f"

COPY patch-open3e-vdens.py /tmp/patch-open3e-vdens.py
RUN python /tmp/patch-open3e-vdens.py

COPY rootfs /
RUN chmod a+x /run.sh /usr/local/bin/open3e_capture

CMD [ "/run.sh" ]

#Labels

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION
ENV BUILD_VERSION="${BUILD_VERSION}"
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="app" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="zcerar5 <ziga.cerar@live.com>" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Home Assistant Add-ons" \
    org.opencontainers.image.authors="zcerar5 <ziga.cerar@live.com>" \
    org.opencontainers.image.licenses="Apache License 2.0" \
    org.opencontainers.image.url="https://github.com/zcerar5/ha-addons" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/open3e_legacy/DOCS.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
