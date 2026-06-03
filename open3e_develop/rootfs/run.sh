#!/usr/bin/with-contenv bashio

bashio::log.info "Preparing Open3e Develop Web UI"

CAN="$(bashio::config 'configurations.can')"
WEB_PORT="$(bashio::config 'configurations.Web_UI_Port')"
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
bashio::log.info "CAN interface: ${CAN}"
bashio::log.info "MQTT host: ${MQTT_HOST}"

if [ -n "${CAN}" ]; then
  bashio::log.info "Preparing CAN interface ${CAN}"
  ip link set down "${CAN}" 2>/dev/null || true
  ip link set "${CAN}" type can bitrate 250000 2>/dev/null || true
  ip link set up "${CAN}" 2>/dev/null || true
fi

export OPEN3E_WEB_PORT="${WEB_PORT}"
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

python3 /seed-web-config.py

bashio::log.info "Starting Open3e Develop Web UI on port ${WEB_PORT}"
cd /data
exec open3e-web
