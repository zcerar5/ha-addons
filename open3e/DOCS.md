# Open3e Add-on Documentation

This add-on installs Open3e from the upstream `develop` branch. By default it runs the legacy Open3e MQTT listener used by the Open3e HACS integration, so Home Assistant controls which datapoints are requested. The Open3e Web UI can be enabled explicitly on port `5051`.

## Requirements

- Home Assistant OS or Home Assistant Supervised.
- Mosquitto broker installed and configured in Home Assistant.
- A CAN adapter connected to the Home Assistant host.

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `can` | `can0` | CAN interface used to communicate with the E3 device. |
| `Web_UI_Enabled` | `false` | Enable Open3e Web UI mode. Keep disabled when using the Open3e HACS integration as the controller. |
| `Web_UI_Port` | `5051` | Port used by the Open3e Web UI when Web UI mode is enabled. |
| `Listen_Topic` | `open3e/cmnd` | MQTT topic where the legacy Open3e listener receives commands from the Open3e HACS integration. |
| `Server_Topic` | `open3e` | MQTT topic where Open3e publishes data. |
| `MQTT_FormatString` | `{device}_{ecuAddr:03X}_{didNumber}_{didName}` | Format used to build MQTT entity topic names. This default matches the original add-on and Open3e HACS integration flow. |
| `MQTT_ClientID` | `open3e` | MQTT client ID used by Open3e. |
| `MQTT_Publish_JSON` | `false` | Web UI mode setting. Keep disabled for Home Assistant so complex datapoints are published as split subtopics. |
| `Auto_Select_HACS_Datapoints` | `true` | Web UI mode setting. Automatically enable the base datapoints used by the Open3e HACS integration. |
| `Auto_Select_Room_Datapoints` | `true` | Web UI mode setting. Automatically enable discovered room temperature and humidity datapoints at low priority. |

When `Web_UI_Enabled` is `false`, the Open3e HACS integration requests system information and feature values through `open3e/cmnd`, as with the original add-on.

When `Web_UI_Enabled` is `true`, open the Web UI from the add-on page or at `http://<home-assistant-host>:5051`. After running System Depiction for the first time, restart the add-on once so the HACS and room presets can apply to the discovered datapoints.

This fork exposes ViCare/ZigBee room device current values in the Vitocal/Vcal and Vitodens/Vdens profiles. That lets Home Assistant create room temperature and humidity entities when those datapoints are present on the bus.

## Support

Open3e upstream discussion: https://github.com/open3e/open3e/discussions/216
