# Open3e Home Assistant Add-on

Use at your own risk. Please share feedback about Open3e in the upstream discussion:
https://github.com/open3e/open3e/discussions/216

Note: the ARMHF image was removed because it is no longer supported by Home Assistant Python base images.

This add-on connects to a USB CAN adapter plugged into the Home Assistant device. It runs the Open3e CAN-to-MQTT application to read and potentially write to Viessmann E3 platform devices such as heat pumps, ventilation systems, and solar inverters.

This fork uses Open3e from upstream `develop` for the classic MQTT listener and exposes ViCare/ZigBee room device current values for the Vdens profile, so the Open3e HACS integration can categorize room temperature and humidity entities.

It requires the Mosquitto MQTT broker to be installed in Home Assistant. The add-on uses the Home Assistant Supervisor MQTT service information to publish and subscribe to data from the CAN adapter.

Usually only the topics need to be adjusted when you do not want to use the defaults:

![Configuration](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e/images/homeassistant-configuration1.jpg)

Options:

- `can`: should usually be `can0`; if not found, check the network interfaces on your Home Assistant host and adjust accordingly.
- `Listen_Topic`: topic where the add-on listens for commands.
- `Server_Topic`: topic where Open3e publishes data.
- `MQTT_FormatString`: leave the default option or check the Open3e documentation for valid options.
- `MQTT_ClientID`: client ID used by the add-on in the MQTT broker.

Startup of the Add-On, where initially the command open3e_depictsystem runs:

![Startup](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e/images/homeassistant-startup.jpg)


Using the Add-On for Demo purposes with the MQTT-Explorer and sending a command to the Listen_Topic Endpoint and seeing the reply on the open3e Topic:

![Running](https://raw.githubusercontent.com/zcerar5/ha-addons/refs/heads/main/open3e/images/homeassistant-running.jpg)





Add-ons only work on Home Assistant OS and Home Assistant Supervised installations. See https://www.home-assistant.io/installation/.
