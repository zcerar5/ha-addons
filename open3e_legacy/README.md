# Open3e Legacy Home Assistant Add-on

Use at your own risk. Please share feedback about Open3e in the upstream discussion:
https://github.com/open3e/open3e/discussions/216

Note: the ARMHF image was removed because it is no longer supported by Home Assistant Python base images.

This add-on connects to a USB CAN adapter plugged into the Home Assistant device. It runs the classic Open3e CAN-to-MQTT listener for the Open3e HACS integration. It does not include or start the Open3e Web UI.

This fork uses Open3e from upstream `develop` for the classic MQTT listener and exposes ViCare/ZigBee room device current values for the Vitocal/Vcal and Vitodens/Vdens profiles, so the Open3e HACS integration can categorize room temperature and humidity entities.

It requires the Mosquitto MQTT broker to be installed in Home Assistant. The add-on uses the Home Assistant Supervisor MQTT service information to publish and subscribe to data from the CAN adapter.

Usually only the topics need to be adjusted when you do not want to use the defaults:

![Configuration](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e_legacy/images/homeassistant-configuration1.jpg)

Options:

- `can`: should usually be `can0`; if not found, check the network interfaces on your Home Assistant host and adjust accordingly.
- `Listen_Topic`: topic where the add-on listens for commands.
- `Server_Topic`: topic where Open3e publishes data.
- `MQTT_FormatString`: leave the default option or check the Open3e documentation for valid options.
- `MQTT_ClientID`: client ID used by the add-on in the MQTT broker.

Startup of the add-on, where initially the command `open3e_depictSystem` runs:

![Startup](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e_legacy/images/homeassistant-startup.jpg)

The add-on also exposes a terminal through the **Open Web UI** button in Home Assistant. This opens a shell inside the Open3e Legacy add-on container for Open3e troubleshooting commands.


Using the Add-On for Demo purposes with the MQTT-Explorer and sending a command to the Listen_Topic Endpoint and seeing the reply on the open3e Topic:

![Running](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e_legacy/images/homeassistant-running.jpg)





Add-ons only work on Home Assistant OS and Home Assistant Supervised installations. See https://www.home-assistant.io/installation/.
