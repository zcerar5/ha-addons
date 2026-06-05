# Open3e Add-on Documentation

This add-on installs Open3e from the upstream `develop` branch. By default it starts the Open3e Web UI on port `5051` and also runs the legacy Open3e MQTT listener used by the Open3e HACS integration.

## Requirements

- Home Assistant OS or Home Assistant Supervised.
- Mosquitto broker installed and configured in Home Assistant.
- A CAN adapter connected to the Home Assistant host.

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `can` | `can0` | CAN interface used to communicate with the E3 device. |
| `Web_UI_Enabled` | `true` | Start Open3e Web UI in addition to the legacy MQTT listener. |
| `Web_UI_Port` | `5051` | Port used by the Open3e Web UI. |
| `Listen_Topic` | `open3e/cmnd` | MQTT topic where the legacy Open3e listener receives commands from the Open3e HACS integration. |
| `Server_Topic` | `open3e` | MQTT topic where Open3e publishes data. |
| `MQTT_FormatString` | `{device}_{ecuAddr:03X}_{didNumber}_{didName}` | Format used to build MQTT entity topic names. This default matches the original add-on and Open3e HACS integration flow. |
| `MQTT_ClientID` | `open3e` | MQTT client ID used by Open3e. |
| `MQTT_Publish_JSON` | `false` | Web UI mode setting. Keep disabled for Home Assistant so complex datapoints are published as split subtopics. |
| `Auto_Select_HACS_Datapoints` | `false` | Web UI mode setting. Preselect the base datapoints used by the Open3e HACS integration. Disabled by default so Open3e HACS remains the polling controller. |
| `Auto_Select_Room_Datapoints` | `false` | Web UI mode setting. Preselect discovered room temperature and humidity datapoints. Disabled by default so Open3e HACS remains the polling controller. |

The Open3e HACS integration requests system information and feature values through `open3e/cmnd`, as with the original add-on. This request-driven path remains active even when the Web UI is enabled.

Open the Web UI from the add-on page or at `http://<home-assistant-host>:5051`. If you use the Web UI to enable polling or publish Home Assistant discovery, it becomes an additional controller alongside Open3e HACS and can create duplicate entities.

This fork exposes ViCare/ZigBee room device current values in the Vitocal/Vcal and Vitodens/Vdens profiles. That lets Home Assistant create room temperature and humidity entities when those datapoints are present on the bus.

## Support

Open3e upstream discussion: https://github.com/open3e/open3e/discussions/216
