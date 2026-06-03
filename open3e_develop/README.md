# Open3e Develop Home Assistant Add-on

This variant installs Open3e from the upstream `develop` branch:
https://github.com/open3e/open3e/tree/develop

It starts the Open3e Web UI on port `5051`.

Use at your own risk. Please share feedback about Open3e in the upstream discussion:
https://github.com/open3e/open3e/discussions/216

Note: the ARMHF image was removed because it is no longer supported by Home Assistant Python base images.

This add-on connects to a USB CAN adapter plugged into the Home Assistant device. It runs the Open3e CAN-to-MQTT application from the upstream develop branch to read and potentially write to Viessmann E3 platform devices such as heat pumps, ventilation systems, and solar inverters.

It requires the Mosquitto MQTT broker to be installed in Home Assistant. The add-on uses the Home Assistant Supervisor MQTT service information to publish and subscribe to data from the CAN adapter.

Usually only the topics need to be adjusted when you do not want to use the defaults:

![Configuration](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e_develop/images/homeassistant-configuration1.jpg)

Options:

- `can`: should usually be `can0`; if not found, check the network interfaces on your Home Assistant host and adjust accordingly.
- `Listen_Topic`: topic where the add-on listens for commands.
- `Server_Topic`: topic where Open3e publishes data.
- `MQTT_FormatString`: leave the default option for Home Assistant discovery.
- `MQTT_ClientID`: client ID used by the add-on in the MQTT broker.
- `MQTT_Publish_JSON`: keep disabled for Home Assistant so complex datapoints are split into subtopics.
- `Auto_Select_HACS_Datapoints`: enables the base datapoints used by the Open3e HACS integration.
- `Auto_Select_Room_Datapoints`: enables discovered room temperature and humidity datapoints at low priority.

Open the add-on Web UI from Home Assistant, or browse to `http://<home-assistant-host>:5051`.

After the first System Depiction scan, restart the add-on once so the HACS and room datapoint presets can apply to the discovered datapoints. Then use the Web UI to apply Home Assistant defaults and publish Home Assistant discovery.

Startup of the Add-On:

![Startup](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e_develop/images/homeassistant-startup.jpg)


Using the Add-On for Demo purposes with the MQTT-Explorer and sending a command to the Listen_Topic Endpoint and seeing the reply on the open3e Topic:

![Running](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e_develop/images/homeassistant-running.jpg)





Add-ons only work on Home Assistant OS and Home Assistant Supervised installations. See https://www.home-assistant.io/installation/.
