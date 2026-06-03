# Open3e Develop Add-on Documentation

This add-on installs Open3e from the upstream `develop` branch:
https://github.com/open3e/open3e/tree/develop

## Requirements

- Home Assistant OS or Home Assistant Supervised.
- Mosquitto broker installed and configured in Home Assistant.
- A CAN adapter connected to the Home Assistant host.

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `can` | `can0` | CAN interface used to communicate with the E3 device. |
| `Listen_Topic` | `open3e-develop/cmnd` | MQTT topic where Open3e listens for commands. |
| `Server_Topic` | `open3e-develop` | MQTT topic where Open3e publishes data. |
| `MQTT_FormatString` | `{device}_{ecuAddr:03X}_{didNumber}_{didName}` | Format used to build MQTT entity topic names. |
| `MQTT_ClientID` | `open3e-develop` | MQTT client ID used by Open3e. |

The first start may take longer because `open3e_depictSystem` creates `/data/devices.json`.

## Support

Open3e upstream discussion: https://github.com/open3e/open3e/discussions/216
