ARG BUILD_FROM=ghcr.io/home-assistant/base-python:3.14-alpine3.23
FROM $BUILD_FROM


RUN apk update && apk add --no-cache git iproute2
RUN mkdir -p /data
WORKDIR /data

# Pinned to the last upstream commit that still contains the Web UI
# (upstream later moved it to the feature/WebUI branch, which points at this
# same commit). Includes the O3ESwitch ZigBee room device codec fixes.
RUN pip install "open3e[web] @ git+https://github.com/open3e/open3e.git@3dba3948f49fc053142b6650b952dcee5802cf81"

COPY patch-open3e-vdens.py /tmp/patch-open3e-vdens.py
RUN python /tmp/patch-open3e-vdens.py
COPY patch-open3e-zigbee-flatten.py /tmp/patch-open3e-zigbee-flatten.py
RUN python /tmp/patch-open3e-zigbee-flatten.py
COPY patch-open3e-vitotrol.py /tmp/patch-open3e-vitotrol.py
RUN python /tmp/patch-open3e-vitotrol.py
COPY patch-open3e-web-terminal.py /tmp/patch-open3e-web-terminal.py
RUN python /tmp/patch-open3e-web-terminal.py
COPY patch-open3e-web-writables.py /tmp/patch-open3e-web-writables.py
RUN python /tmp/patch-open3e-web-writables.py
COPY patch-open3e-web-ha-defaults.py /tmp/patch-open3e-web-ha-defaults.py
RUN python /tmp/patch-open3e-web-ha-defaults.py

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
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/open3e/DOCS.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
