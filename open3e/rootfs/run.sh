#!/usr/bin/with-contenv bashio


bashio::log.info "Preparing to start...reading config"


CAN=$(bashio::config 'configurations.can')
bashio::log.info "Can Interface:  $CAN"
LISTENTOPIC=$(bashio::config 'configurations.Listen_Topic')
bashio::log.info "Listen to topic:  $LISTENTOPIC"
TOPIC=$(bashio::config 'configurations.Server_Topic')
bashio::log.info "MQTT Server and Publish Topic:  $TOPIC"
FORMATSTRING=$(bashio::config 'configurations.MQTT_FormatString')
bashio::log.info "Format String:  $FORMATSTRING"
CLIENTID=$(bashio::config 'configurations.MQTT_ClientID')
bashio::log.info "ClientID:  $CLIENTID"    

MQTT_HOST=$(bashio::services mqtt "host")
MQTT_USER=$(bashio::services mqtt "username")
MQTT_PASSWORD=$(bashio::services mqtt "password")

bashio::log.info "MQTT data from API:  Host: $MQTT_HOST  User: $MQTT_USER"

bashio::log.info "Preparing to start...checking can interface"

ip link set down $CAN && ip link set $CAN type can bitrate 250000 && ip link set up $CAN
ip link | grep $CAN

bashio::log.info "Preparing to start...checking for devices.json"

if ! test -f /data/devices.json; then
   bashio::log.info "Running open3e_depictSystem -c $CAN ... This may take a while"
   cd /data
   open3e_depictSystem -c $CAN
fi

bashio::log.info "Starting Open3e... open3e --can $CAN --mqtt $MQTT_HOST:1883:$TOPIC --mqttuser redacted! --mqttformatstring $FORMATSTRING --mqttclientid $CLIENTID --listen $LISTENTOPIC --config /data/devices.json"
cd /data
open3e --can $CAN --mqtt $MQTT_HOST:1883:$TOPIC --mqttuser $MQTT_USER:$MQTT_PASSWORD --mqttformatstring $FORMATSTRING --mqttclientid $CLIENTID --listen $LISTENTOPIC --config /data/devices.json
