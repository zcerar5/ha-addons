#!/usr/bin/with-contenv bashio

bashio::log.info "Preparing Open3e"

CAN="$(bashio::config 'configurations.can')"
WEB_ENABLED="$(bashio::config 'configurations.Web_UI_Enabled')"
CONTROLLER_MODE="$(bashio::config 'configurations.Controller_Mode')"
WEB_PORT="$(bashio::config 'configurations.Web_UI_Port')"
LISTENTOPIC="$(bashio::config 'configurations.Listen_Topic')"
TOPIC="$(bashio::config 'configurations.Server_Topic')"
FORMATSTRING="$(bashio::config 'configurations.MQTT_FormatString')"
CLIENTID="$(bashio::config 'configurations.MQTT_ClientID')"
PUBLISH_JSON="$(bashio::config 'configurations.MQTT_Publish_JSON')"
AUTO_HACS_DPS="$(bashio::config 'configurations.Auto_Select_HACS_Datapoints')"
AUTO_ROOM_DPS="$(bashio::config 'configurations.Auto_Select_Room_Datapoints')"

MQTT_HOST="$(bashio::services mqtt "host")"
MQTT_USER="$(bashio::services mqtt "username")"
MQTT_PASSWORD="$(bashio::services mqtt "password")"

bashio::log.info "Web UI port: ${WEB_PORT}"
bashio::log.info "Web UI enabled: ${WEB_ENABLED}"
bashio::log.info "Controller mode: ${CONTROLLER_MODE}"
bashio::log.info "CAN interface: ${CAN}"
bashio::log.info "MQTT host: ${MQTT_HOST}"
bashio::log.info "MQTT listen topic: ${LISTENTOPIC}"
bashio::log.info "MQTT topic prefix: ${TOPIC}"
bashio::log.info "MQTT format string: ${FORMATSTRING}"
bashio::log.info "MQTT client ID: ${CLIENTID}"

if [ -n "${CAN}" ]; then
  bashio::log.info "Preparing CAN interface ${CAN}"
  ip link set down "${CAN}" 2>/dev/null || true
  ip link set "${CAN}" type can bitrate 250000 2>/dev/null || true
  ip link set up "${CAN}" 2>/dev/null || true
fi

WEB_PID=""
LEGACY_PID=""

stop_children() {
  bashio::log.info "Stopping Open3e processes"
  if [ -n "${LEGACY_PID}" ]; then
    kill "${LEGACY_PID}" 2>/dev/null || true
  fi
  if [ -n "${WEB_PID}" ]; then
    kill "${WEB_PID}" 2>/dev/null || true
  fi
}

trap stop_children TERM INT

if [ "${WEB_ENABLED}" = "true" ]; then
  export OPEN3E_WEB_PORT="${WEB_PORT}"

  if [ "${CONTROLLER_MODE}" = "open3e-ha" ]; then
    export OPEN3E_WEB_PASSIVE="true"
    bashio::log.info "Starting Web UI in passive mode; Open3e HACS controls CAN polling through MQTT commands"
  else
    export OPEN3E_WEB_PASSIVE="false"
    export OPEN3E_CAN_INTERFACE="${CAN}"
    export OPEN3E_CAN_BITRATE="250000"
    export OPEN3E_MQTT_HOST="${MQTT_HOST}"
    export OPEN3E_MQTT_PORT="1883"
    export OPEN3E_MQTT_USER="${MQTT_USER}"
    export OPEN3E_MQTT_PASSWORD="${MQTT_PASSWORD}"
    export OPEN3E_MQTT_TOPIC_PREFIX="${TOPIC}"
    export OPEN3E_MQTT_FORMAT_STRING="${FORMATSTRING}"
    export OPEN3E_MQTT_CLIENT_ID="${CLIENTID}"
    export OPEN3E_MQTT_PUBLISH_JSON="${PUBLISH_JSON}"
    export OPEN3E_AUTO_SELECT_HACS_DATAPOINTS="${AUTO_HACS_DPS}"
    export OPEN3E_AUTO_SELECT_ROOM_DATAPOINTS="${AUTO_ROOM_DPS}"
  fi

  python3 /seed-web-config.py

  bashio::log.info "Starting Open3e Web UI on port ${WEB_PORT}"
  cd /data
  open3e-web &
  WEB_PID="$!"
fi

if [ "${CONTROLLER_MODE}" = "open3e-ha" ] || [ "${WEB_ENABLED}" != "true" ]; then
  if ! test -f /data/devices.json; then
    bashio::log.info "Running open3e_depictSystem -c ${CAN} ... This may take a while"
    cd /data
    open3e_depictSystem -c "${CAN}"
  fi

  bashio::log.info "Starting Open3e legacy listener: topic=${TOPIC}, listen=${LISTENTOPIC}"
  cd /data
  open3e \
    --can "${CAN}" \
    --mqtt "${MQTT_HOST}:1883:${TOPIC}" \
    --mqttuser "${MQTT_USER}:${MQTT_PASSWORD}" \
    --mqttformatstring "${FORMATSTRING}" \
    --mqttclientid "${CLIENTID}" \
    --listen "${LISTENTOPIC}" \
    --config /data/devices.json &
  LEGACY_PID="$!"
fi

if [ -n "${LEGACY_PID}" ]; then
  wait "${LEGACY_PID}"
  STATUS="$?"
elif [ -n "${WEB_PID}" ]; then
  wait "${WEB_PID}"
  STATUS="$?"
else
  bashio::log.error "Neither Web UI nor legacy Open3e listener is enabled"
  STATUS="1"
fi
stop_children
exit "${STATUS}"
