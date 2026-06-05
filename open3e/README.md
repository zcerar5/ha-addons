# Open3e Home Assistant Add-on

Use at your own risk. Please share feedback about Open3e in the upstream discussion:
https://github.com/open3e/open3e/discussions/216

Note: the ARMHF image was removed because it is no longer supported by Home Assistant Python base images.

This add-on connects to a USB CAN adapter plugged into the Home Assistant device. By default it starts the Open3e Web UI and lets the Web UI control which datapoints are requested and published to Home Assistant.

This fork uses Open3e from upstream `develop`, keeps optional Web UI support, and exposes ViCare/ZigBee room device current values for the Vitocal/Vcal and Vitodens/Vdens profiles, so Home Assistant can categorize room temperature and humidity entities.

It requires the Mosquitto MQTT broker to be installed in Home Assistant. The add-on uses the Home Assistant Supervisor MQTT service information to publish and subscribe to data from the CAN adapter.

Usually only the topics need to be adjusted when you do not want to use the defaults:

![Configuration](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e/images/homeassistant-configuration1.jpg)

Options:

- `can`: should usually be `can0`; if not found, check the network interfaces on your Home Assistant host and adjust accordingly.
- `Web_UI_Enabled`: starts the Open3e Web UI.
- `Controller_Mode`: use `webui` when the Open3e Web UI should control CAN polling and MQTT publishing. Use `open3e-ha` when the Open3e HACS integration should control polling through the legacy MQTT command listener.
- `Web_UI_Port`: port used by the Open3e Web UI.
- `Listen_Topic`: topic where the add-on listens for Open3e HACS integration commands.
- `Server_Topic`: topic where Open3e publishes data.
- `MQTT_FormatString`: leave the default option for Open3e HACS compatibility.
- `MQTT_ClientID`: client ID used by the add-on in the MQTT broker.
- `MQTT_Publish_JSON`: Web UI mode setting; keep disabled for Home Assistant so complex datapoints are split into subtopics.
- `Auto_Select_HACS_Datapoints`: Web UI mode setting; disabled by default so Open3e HACS remains the polling controller.
- `Auto_Select_Room_Datapoints`: Web UI mode setting; disabled by default so Open3e HACS remains the polling controller.

In `open3e-ha` controller mode, Open3e HACS requests system information and feature values through `open3e/cmnd`, as with the original add-on. The Web UI still opens, but it is kept passive so it does not also control CAN/MQTT.

Open the add-on Web UI from Home Assistant, or browse to `http://<home-assistant-host>:5051`.

Startup of the add-on:

![Startup](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e/images/homeassistant-startup.jpg)


Using the Add-On for Demo purposes with the MQTT-Explorer and sending a command to the Listen_Topic Endpoint and seeing the reply on the open3e Topic:

![Running](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e/images/homeassistant-running.jpg)





Add-ons only work on Home Assistant OS and Home Assistant Supervised installations. See https://www.home-assistant.io/installation/.
