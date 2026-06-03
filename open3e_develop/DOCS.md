# Open3e Develop Add-on Documentation

This add-on installs Open3e from the upstream `develop` branch:
https://github.com/open3e/open3e/tree/develop

The add-on starts the Open3e Web UI on port `5051`.

## Requirements

- Home Assistant OS or Home Assistant Supervised.
- Mosquitto broker installed and configured in Home Assistant.
- A CAN adapter connected to the Home Assistant host.

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `can` | `can0` | CAN interface used to communicate with the E3 device. |
| `Web_UI_Port` | `5051` | Port used by the Open3e Web UI. |
| `Listen_Topic` | `open3e_develop/cmnd` | MQTT topic where Open3e listens for commands. |
| `Server_Topic` | `open3e_develop` | MQTT topic where Open3e publishes data. |
| `MQTT_FormatString` | `{didNumber}_{didName}` | Format used to build MQTT entity topic names. This default matches the Web UI Home Assistant discovery topics. |
| `MQTT_ClientID` | `open3e_develop` | MQTT client ID used by Open3e. |
| `MQTT_Publish_JSON` | `false` | Keep disabled for Home Assistant so complex datapoints are published as split subtopics. |
| `Auto_Select_Room_Datapoints` | `true` | Automatically enable discovered room temperature and humidity datapoints at low priority. |

Open the Web UI from the add-on page or at `http://<home-assistant-host>:5051`.

After running System Depiction for the first time, restart the add-on once so the room preset can apply to the discovered datapoints. Then publish Home Assistant discovery from the Web UI.

## Support

Open3e upstream discussion: https://github.com/open3e/open3e/discussions/216
